import os
import sys
import re
import json
import subprocess
import yaml
from drivers import github_client, git_client
from kernel import agent_frontier, daemon_prompt, daemon_backlog, daemon_nba
from kernel.daemon_telemetry import TelemetryDaemon, record_execution
from kernel.daemon_transaction import FlowTransaction

def is_verbose() -> bool:
    """Checks if verbose mode is triggered by the operator."""
    return os.environ.get("SPAO_VERBOSE") in ("1", "true", "TRUE") or os.environ.get("SPOA_VERBOSE") in ("1", "true", "TRUE")

def load_node_status_config() -> dict:
    """Loads the node status mapping from node.yml."""
    from drivers import path_resolver
    config = path_resolver.load_node_yml()
    return config.get("node_attributes", {}).get("status", {})

def load_node_classification_config() -> dict:
    """Loads the node classification mapping from node.yml."""
    from drivers import path_resolver
    config = path_resolver.load_node_yml()
    return config.get("node_attributes", {}).get("classification", {})


def log_stage_advancement(stage: str, status: str, details: str = "") -> None:
    """Prints a beautiful H1 banner representing SPAO loop stage advancement when verbose is active."""
    stage_colors = {
        "sense": "🔍 SENSE",
        "plan": "📋 PLAN",
        "act": "⚡ ACT",
        "observe": "👀 OBSERVE",
        "reflect": "💾 REFLECT"
    }
    stage_label = stage_colors.get(stage.lower(), stage.upper())
    
    if not is_verbose():
        msg = f"[{stage_label}] {status}"
        if details:
            msg += f" - {details}"
        print(msg, file=sys.stdout, flush=True)
        return

    print("\n" + "═"*60, file=sys.stdout, flush=True)
    print(f" 🔄 SPAO Loop Stage  ►  {stage_label}", file=sys.stdout, flush=True)
    print(f" 📌 Status           ►  {status}", file=sys.stdout, flush=True)
    if details:
        print(f" 📝 Details          ►  {details}", file=sys.stdout, flush=True)
    print("═"*60 + "\n", file=sys.stdout, flush=True)

class BaseNode:
    """Abstract base class for all Antigravity Nodes."""
    def __init__(self, issue_id: str):
        self.issue_id = str(issue_id)
        
    @property
    def gh_labels(self):
        return github_client.get_issue_labels(self.issue_id)

    @property
    def loop(self) -> str | None:
        try:
            for label in self.gh_labels:
                if label.startswith("loop:"):
                    return label.split(":", 1)[1].strip()
        except Exception:
            pass
        return None

    @property
    def area(self) -> str | None:
        try:
            for label in self.gh_labels:
                if label.startswith("area:"):
                    return label.split(":", 1)[1].strip()
        except Exception:
            pass
        return None

    @property
    def kind(self) -> str | None:
        try:
            for label in self.gh_labels:
                if label.startswith("kind:"):
                    return label.split(":", 1)[1].strip()
        except Exception:
            pass
        return None

    def get_worktree_path(self, branch_name: str) -> str:
        workspace_dir = os.environ.get("SPAO_WORKSPACE_DIR")
        if workspace_dir:
            return os.path.join(os.path.abspath(workspace_dir), ".worktrees", branch_name)
        
        loop_val = self.loop
        if loop_val == "spao":
            return os.path.join(".worktrees", "spao", branch_name)
        elif loop_val == "sdlc":
            return os.path.join(".worktrees", "sdlc", branch_name)
        else:
            return os.path.join(".worktrees", branch_name)
        
    def add_gh_label(self, label: str):
        github_client.add_label(self.issue_id, label)
        
    def update_body(self, body: str):
        github_client.update_issue_body(self.issue_id, body)
        
    def close(self, comment: str):
        github_client.close_issue(self.issue_id, comment)

    def reopen(self, comment: str = ""):
        github_client.reopen_issue(self.issue_id)

    def set_status(self, status_key: str) -> None:
        """Translates a logical status key into a physical label using node.yml and removes other status labels."""
        status_config = load_node_status_config()
        if status_key not in status_config:
            raise ValueError(f"Status key '{status_key}' is not defined in node.yml")
        
        target_label = status_config[status_key]
        try:
            current_labels = self.gh_labels
            for key, label in status_config.items():
                if label != target_label and label in current_labels:
                    github_client.remove_label(self.issue_id, label)
        except Exception:
            pass
            
        self.add_gh_label(target_label)

    def set_classification(self, classification_key: str) -> None:
        """Translates a logical classification key into a physical label using node.yml."""
        class_config = load_node_classification_config()
        if classification_key not in class_config:
            raise ValueError(f"Classification key '{classification_key}' is not defined in node.yml")
        self.add_gh_label(class_config[classification_key])

class NonTerminalNode(BaseNode):
    """Represents a composite or path node."""
    pass

class TerminalNode(BaseNode):
    """Represents an actionable, execution-level leaf node."""
    
    def __init__(self, issue_id: str):
        super().__init__(issue_id)

    def _verify_state_purity(self, frontier_file: str = "artifacts/frontier_state.md", expected_active: str | None = None):
        """
        Verifies that the frontier state is 'pure' (no conflicting active nodes).
        If expected_active is provided, it validates that the specific node is the only active one.
        """
        if not os.path.exists(frontier_file):
            return
            
        current_active = agent_frontier.read_active_node(frontier_file)
        if current_active and current_active != "None":
            # If we expect a specific node (e.g. during reflect), it must match
            if expected_active and current_active == expected_active:
                return
            
            # Special case for "Node <ID>: Title" format
            match = re.search(r"Node (\d+):", current_active)
            active_id = match.group(1) if match else None
            
            if expected_active and active_id and str(expected_active) == str(active_id):
                return
                
            sys.exit(f"[🚫 BLOCKED] State Dissonance: Cannot proceed because Node '{current_active}' is already marked as active in {frontier_file}. Release the lock first.")

    def _validate_spao_purity(self, worktree_path: str | None = None):
        """Validates that a loop:spao branch only modifies policy/documentation paths."""
        from drivers import path_resolver
        config = path_resolver.load_engine_config()
        enforce = config.get("governance", {}).get("spao_purity_enforcement", True)
        
        try:
            modified_files = git_client.diff_names("main", cwd=worktree_path)
            violations = []
            for filepath in modified_files:
                if filepath.startswith("kb/") or filepath.startswith("artifacts/") or filepath == "GEMINI.md":
                    continue
                violations.append(filepath)
                
            if violations:
                msg = f"SPAO PR Purity Violation: The following executable/code files were modified on a spao-loop branch: {violations}"
                if enforce:
                    raise Exception(msg)
                else:
                    print(f"Warning: {msg}")
        except Exception as e:
            if "SPAO PR Purity Violation" in str(e):
                raise

    def _validate_orthogonal_scope(self):
        """Validates that the current node does not have an identical footprint to another open node."""
        current_node = github_client.get_issue_details(self.issue_id)
        current_title = current_node.get("title", "")
        current_body = current_node.get("body", "")
        
        def extract_goal(body: str) -> str:
            match = re.search(r"## Goal\n(.*?)(?=\n## |\Z)", body, re.DOTALL | re.IGNORECASE)
            return match.group(1).strip().lower() if match else ""
            
        def extract_core_title(title: str) -> str:
            clean = re.sub(r"^(Node \d+: )?(Activity|Discovery|Path)( \d+)?: ", "", title, flags=re.IGNORECASE)
            return clean.strip().lower()

        current_goal = extract_goal(current_body)
        current_core_title = extract_core_title(current_title)
        
        if not current_core_title and not current_goal:
            return
            
        open_issues = github_client.get_open_issues()
        
        for issue in open_issues:
            if str(issue["number"]) == str(self.issue_id):
                continue
                
            other_core_title = extract_core_title(issue.get("title", ""))
            other_goal = extract_goal(issue.get("body", ""))
            
            if current_core_title and current_core_title == other_core_title:
                sys.exit(f"[🚫 BLOCKED] Orthogonal Scope Violation: Node {self.issue_id} has an identical title footprint to Node {issue['number']}")
                
            if current_goal and current_goal == other_goal:
                sys.exit(f"[🚫 BLOCKED] Orthogonal Scope Violation: Node {self.issue_id} has an identical goal footprint to Node {issue['number']}")

    @record_execution(stage="plan")
    def plan_start(self, frontier_file: str = "artifacts/frontier_state.md") -> None:
        from drivers import path_resolver
        if not os.path.isabs(frontier_file):
            frontier_file = path_resolver.resolve_workspace_path(frontier_file)
        with FlowTransaction(frontier_file) as tx:
            self._verify_state_purity(frontier_file)
            
            # Enforce Quarantine Gate: Only allow nodes that possess the 'backlog' label.
            labels = self.gh_labels
            if "backlog" not in labels:
                details = github_client.get_issue_details(self.issue_id)
                current_title = details.get("title", "")
                if re.match(r"^(Node \d+: )?(Activity|Discovery)( \d+)?:", current_title, re.IGNORECASE):
                    self.add_gh_label("backlog")
                else:
                    sys.exit(
                        f"[🚫 BLOCKED] Quarantine Protocol Violation: Node #{self.issue_id} does not possess the 'backlog' label. "
                        f"Current labels: {labels}. Quarantined intake requirements must be promoted by the Operator first."
                    )
            
            open_prs = github_client.get_open_prs()
            if open_prs:
                pr_info = [f"PR #{pr.get('number', 'Unknown')} (branch: {pr.get('headRefName', 'Unknown')})" for pr in open_prs]
                sys.exit(f"[🚫 BLOCKED] WIP-N=1 Invariant Violation: Cannot plan node #{self.issue_id} because there are open pull requests: {pr_info}. You must merge or close them first.")
            
            from kernel.daemon_strategic import verify_node_transition_allowed
            verify_node_transition_allowed(self.issue_id)
            
            in_progress_label = load_node_status_config().get("in_progress", "status: in-progress")
            if in_progress_label in self.gh_labels:
                sys.exit(f"[🚫 BLOCKED] Node #{self.issue_id} is already in progress by another thread!")
                
            # Verify dependencies
            details = github_client.get_issue_details(self.issue_id)
            body = details.get("body", "")
            
            # Find dependencies under "## Depends On"
            dep_match = re.search(r"## Depends On\s*\n+([^\n#]+)", body, re.IGNORECASE)
            if dep_match:
                dep_content = dep_match.group(1).strip()
                if dep_content.upper() != "TBD" and dep_content:
                    dep_ids = re.findall(r"\d+", dep_content)
                    for dep_id in dep_ids:
                        try:
                            dep_details = github_client.get_issue_details(dep_id)
                            if dep_details.get("state") != "CLOSED":
                                sys.exit(f"[🚫 BLOCKED] Dependency Violation: Node #{self.issue_id} depends on Node #{dep_id}, which is still open!")
                        except Exception as e:
                            if "Dependency Violation" in str(e):
                                raise
                            pass
                            
            self._validate_orthogonal_scope()
                
            self.set_status("in_progress")
            tx.register_rollback(self.set_status, "open")
            
            # Atomically set active node in frontier
            node_title = details.get("title", f"Node {self.issue_id}")
            agent_frontier.append_active_node(frontier_file, int(self.issue_id), node_title, "Planning Phase", [])
            
            log_stage_advancement("plan", "Plan-Start Executed", f"Acquired lock on Node #{self.issue_id} and updated frontier.")

    @record_execution(stage="plan")
    def plan_finish(self, body: str) -> str:
        log_stage_advancement("plan", "Formulating Implementation Contract", f"Locking Node Contract into Issue #{self.issue_id}")
        
        issue_details = github_client.get_issue_details(self.issue_id)
        current_title = issue_details.get("title", "")
        
        # Enforce WHAT- spec file tracking in git
        if "plan" in current_title.lower():
            try:
                res = subprocess.run(["git", "diff", "--name-only", "main"], capture_output=True, text=True)
                if res.returncode != 0:
                    res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
                    
                if res.returncode == 0 and res.stdout != "success":
                    modified_files = []
                    if isinstance(res.stdout, str):
                        for line in res.stdout.splitlines():
                            parts = line.strip().split(None, 1)
                            if len(parts) > 1:
                                modified_files.append(parts[1])
                            else:
                                modified_files.append(line.strip())
                                
                    has_spec = any(f.startswith("kb/WHAT-") and f.endswith(".md") for f in modified_files)
                    if not has_spec:
                        sys.exit("[🚫 BLOCKED] SPEC file violation: A corresponding WHAT- specification file under kb/ (e.g. kb/WHAT-*.md) must be created and modified/added to finish the Plan phase.")
            except Exception as e:
                if "SPEC file violation" in str(e):
                    raise
        
        # Enforce static KB conflict checks (SG-0005)
        from kernel import daemon_knowledge_accrual
        from drivers import path_resolver
        daemon_knowledge_accrual.run_kb_check(repo_root=path_resolver.get_workspace_dir(), strict=True)
        
        # Removed logic that previously added "Node <ID>:" to issue titles.
            
        self.update_body(body)
        
        issue_url = f"https://github.com/pltrinh1122/dyad-wu-wei/issues/{self.issue_id}"
        log_stage_advancement("plan", "Plan Phase Completed", f"Node issue #{self.issue_id} successfully planned. Transitioning to Act phase.")
        return issue_url

    @record_execution(stage="act")
    def checkout(self, branch_name: str, frontier_file: str = "artifacts/frontier_state.md") -> None:
        if not os.environ.get("SPAO_WORKSPACE_DIR") and not re.match(r"^node/\d+-[a-z0-9-]+$", branch_name):
            raise ValueError("Branch name MUST follow the standard: node/<id>-<kebab-case>")
            
        from kernel.daemon_strategic import verify_node_transition_allowed
        verify_node_transition_allowed(self.issue_id)

        from drivers import path_resolver
        if not os.path.isabs(frontier_file):
            frontier_file = path_resolver.resolve_workspace_path(frontier_file)

        with FlowTransaction(frontier_file) as tx:
            self._verify_state_purity(frontier_file, expected_active=self.issue_id)
            
            open_prs = github_client.get_open_prs()
            if open_prs:
                pr_info = [f"PR #{pr.get('number', 'Unknown')} (branch: {pr.get('headRefName', 'Unknown')})" for pr in open_prs]
                sys.exit(f"[🚫 BLOCKED] WIP-N=1 Invariant Violation: Cannot checkout node #{self.issue_id} because there are open pull requests: {pr_info}. You must merge or close them first.")
            
            self.set_status("in_progress")
            tx.register_rollback(self.set_status, "open")
            
            worktree_path = self.get_worktree_path(branch_name)
            log_stage_advancement("act", "Initializing Execution Worktree", f"Creating git worktree at {worktree_path}")
            
            os.makedirs(os.path.dirname(worktree_path), exist_ok=True)
            
            git_client.fetch("origin")
            git_client.worktree_add(branch_name, worktree_path, "origin/main")
            tx.register_rollback(git_client.worktree_remove, worktree_path, force=True)
            tx.register_rollback(git_client.branch_delete, branch_name)

            # Sync frontier state updates to worktree so the worktree has the active planning state (Node 1080)
            try:
                import shutil
                rel_workspace = os.environ.get("SPAO_WORKSPACE_DIR", "")
                if rel_workspace and os.path.isabs(rel_workspace):
                    core_dir = path_resolver.get_core_dir()
                    if rel_workspace.startswith(core_dir):
                        rel_workspace = os.path.relpath(rel_workspace, core_dir)

                for ext in [".yml", ".yml.sha256", ".md"]:
                    src = path_resolver.resolve_workspace_path("artifacts", f"frontier_state{ext}")
                    dest = os.path.join(worktree_path, rel_workspace, "artifacts", f"frontier_state{ext}")
                    dest_abs = os.path.abspath(dest)
                    if os.path.exists(src):
                        os.makedirs(os.path.dirname(dest_abs), exist_ok=True)
                        shutil.copy2(src, dest_abs)
                        # Revert uncommitted frontier updates in the root repository to keep main clean (Node 1080)
                        try:
                            git_client.restore([src])
                        except Exception as restore_err:
                            print(f"Warning: Failed to restore root frontier file {src}: {restore_err}")
            except Exception as e:
                print(f"Warning: Failed to sync frontier state to worktree during checkout: {e}")
            
            print(f"\nWorktree established. Please `cd {worktree_path}` to begin work.")

    @record_execution(stage="abort")
    def abort(self, frontier_file: str = "artifacts/frontier_state.md") -> None:
        from drivers import path_resolver
        if not os.path.isabs(frontier_file):
            frontier_file = path_resolver.resolve_workspace_path(frontier_file)

        with FlowTransaction(frontier_file) as tx:
            log_stage_advancement("abort", "Initiating Abort Phase", f"Releasing lock on Issue #{self.issue_id}")
            
            # Remove in-progress label and restore 'open' status
            try:
                self.set_status("open")
            except Exception as e:
                print(f"Warning: Failed to set status to open: {e}")
                
            # Discard any associated worktrees
            branches = [f"node/{self.issue_id}-plan", f"node/{self.issue_id}-act", f"node/{self.issue_id}-observe"]
            for branch_name in branches:
                wt_path = self.get_worktree_path(branch_name)
                if os.path.exists(wt_path):
                    try:
                        git_client.worktree_remove(wt_path, force=True)
                    except Exception as e:
                        print(f"Warning: Failed to remove worktree {wt_path}: {e}")
                try:
                    if branch_name in git_client.list_local_branches():
                        git_client.branch_delete(branch_name)
                except Exception:
                    pass
            
            # Revert the active node entry
            agent_frontier.abort_active_node(frontier_file, str(self.issue_id))

    def reflect(self, frontier_file: str, node_name: str, learnings: str, invariants: list[str], commit_msg: str, branch_name: str, stage: str = "all", insights: str = "") -> None:
        if not os.environ.get("SPAO_WORKSPACE_DIR") and not re.match(r"^node/\d+-[a-z0-9-]+$", branch_name):
            raise ValueError("Branch name MUST follow the standard: node/<id>-<kebab-case>")
 
        from drivers import path_resolver
        if not os.path.isabs(frontier_file):
            frontier_file = path_resolver.resolve_workspace_path(frontier_file)

        main_repo = path_resolver.get_core_dir()
        workspace_dir = os.environ.get("SPAO_WORKSPACE_DIR")
        if workspace_dir:
            worktree_dir = os.path.abspath(self.get_worktree_path(branch_name))
        else:
            worktree_dir = os.path.abspath(os.path.join(main_repo, self.get_worktree_path(branch_name)))

        # Redirect frontier_file to mutate directly inside the worktree checkout (Node 1080)
        try:
            workspace_root = path_resolver.resolve_workspace_path("")
            if os.path.abspath(frontier_file).startswith(os.path.abspath(workspace_root)):
                rel_workspace = os.environ.get("SPAO_WORKSPACE_DIR", "")
                if rel_workspace and os.path.isabs(rel_workspace):
                    core_dir = path_resolver.get_core_dir()
                    if rel_workspace.startswith(core_dir):
                        rel_workspace = os.path.relpath(rel_workspace, core_dir)

                rel_frontier = os.path.relpath(frontier_file, workspace_root)
                frontier_file = os.path.abspath(os.path.join(worktree_dir, rel_workspace, rel_frontier))
        except Exception as e:
            print(f"Warning: Failed to redirect frontier_file to worktree: {e}")

        with FlowTransaction(frontier_file) as tx:
            log_stage_advancement("reflect", "Initiating Reflect Phase", f"Closing Issue #{self.issue_id}, updating ledger, and preparing branch: '{branch_name}'")
            
            from kernel.daemon_strategic import verify_node_transition_allowed
            verify_node_transition_allowed(self.issue_id)
            
            # Enforce Prevent Empty PR Guard (Node 1437)
            status_output = git_client.status_porcelain(cwd=worktree_dir).strip()
            diff_against_main = git_client.diff_names("origin/main", cwd=worktree_dir)
            if not status_output and not diff_against_main:
                sys.exit("[🚫 BLOCKED] Reflection Blocked: No file changes detected. You cannot reflect an empty PR. Please implement the required changes before reflecting.")
            
            # Enforce Conflict-Free Reflection Invariant (WHY-0083)
            git_client.fetch("origin")
            if git_client.check_merge_conflicts("origin/main", cwd=worktree_dir):
                sys.exit(f"[🚫 BLOCKED] Reflection Blocked (WHY-0083): Branch '{branch_name}' has unresolved merge conflicts with 'origin/main'. You must resolve these conflicts locally before reflecting.")
            
            # Enforce Local CI Verification Invariant
            try:
                import subprocess
                print("Running local test suite verification before reflection...")
                run_tests_script = os.path.join(worktree_dir, "bin", "run-tests")
                if not os.path.exists(run_tests_script):
                    run_tests_script = os.path.join(main_repo, "bin", "run-tests")
                subprocess.run([run_tests_script], cwd=worktree_dir, check=True)
                print("Local test suite passed.")
            except subprocess.CalledProcessError:
                sys.exit("[🚫 BLOCKED] Reflection Blocked: Local test suite verification failed. You must remediate CI failures before reflecting.")

            # Enforce post-failure reflection gate (SG-0005)
            from kernel import daemon_knowledge_accrual
            daemon_knowledge_accrual.enforce_reflection_hook(self.issue_id, repo_root=main_repo, worktree_root=worktree_dir)
            
            self.close("Node completed via Node Lifecycle Daemon. Moving to PR.")
            tx.register_rollback(self.reopen)
            
            # Automate Meta-Index Checkbox Synchronization
            active_path_str = agent_frontier.read_active_path(frontier_file)
            if active_path_str:
                path_issue_id = agent_frontier.extract_path_id(active_path_str)
                if path_issue_id:
                    backlog = daemon_backlog.BacklogDaemon()
                    backlog.check_off_meta_index(path_issue_id, self.issue_id)
                    tx.register_rollback(backlog.uncheck_meta_index, path_issue_id, self.issue_id)
                else:
                    print(f"Warning: Failed to extract Path ID from active path string: '{active_path_str}'")
            
            # ATOMIC UPDATE: Mark node completed AND clear pointers
            agent_frontier.complete_active_node(frontier_file, node_name, learnings, invariants, clear_pointers=True)
            
            # Enforce Path Invariant: Evaluate the active path and close it if 0 activities remain
            nba = daemon_nba.NBADaemon()
            nba_result = nba.evaluate(frontier_file=frontier_file)
            
            clear_path = False
            if nba_result["type"] == "path_switching" and active_path_str:
                # We had an active path, but NBA now says we should switch (because it's exhausted)
                path_issue_id = agent_frontier.extract_path_id(active_path_str)
                if path_issue_id:
                    github_client.close_issue(path_issue_id, "Path Invariant Enforced: Automatically closed because the final child Activity has been completed.")
                    tx.register_rollback(github_client.reopen_issue, path_issue_id)
                    log_stage_advancement("reflect", "Path Invariant Enforced", f"Automatically closed parent {active_path_str}")
                    clear_path = True
            
            if clear_path:
                agent_frontier.set_active_path(frontier_file, "None")
            
            # The frontier state files were updated directly inside the worktree (Node 1080), so copying from root is unnecessary.
            pass
            
            # Run SPAO purity validation check before git commit/push
            if self.loop == "spao":
                self._validate_spao_purity(worktree_path=worktree_dir)
            
            # Execute staging strategy
            if stage == "none":
                pass
            elif stage == "all":
                git_client.add(["."], cwd=worktree_dir)
            else:
                files_to_stage = [f.strip() for f in stage.split(",") if f.strip()]
                if files_to_stage:
                    git_client.add(files_to_stage, cwd=worktree_dir)

            git_client.commit(commit_msg, cwd=worktree_dir)
            # rollback the local commit if remote operations fail
            tx.register_rollback(git_client.reset_hard, cwd=worktree_dir)

            # Rebase onto origin/main with auto-resolution of deterministic conflicts (Node 808)
            git_client.fetch("origin", cwd=worktree_dir)
            git_client.rebase_with_conflict_resolution("origin/main", cwd=worktree_dir)


            git_client.push(branch_name, cwd=worktree_dir)
            
            loop_val = (self.loop or "unknown").upper()
            transition_summary = f"""

## Three-Loop Transition Summary
- **Source Loop**: {loop_val}
- **Target Lineage**: main
- **Gate Status**: Gate-1 [OK], Gate-2 [OK]

### Observed Variances & Recommendations
- None."""
            
            pr_body = f"Resolves #{self.issue_id}\n\n{learnings}{transition_summary}"
            if insights:
                pr_body += f"\n\nActive-Insights: {insights}"
            
            from kernel.title_utils import clean_node_title
            clean_name = clean_node_title(node_name)
            pr_title = f"PR: {clean_name}"
            pr_url = github_client.create_pull_request(pr_title, pr_body, head=branch_name)
            
            # Evaluate Administrative Node HTIL Bypass (WHY-0087-universal-merge-gate-bypass)
            modified_files = git_client.diff_names("origin/main", cwd=worktree_dir)
            is_autonomous_merge = False
            if not modified_files:
                is_autonomous_merge = True
            elif all(f.startswith("artifacts/") and "template" not in f.lower() for f in modified_files):
                is_autonomous_merge = True
            elif "act" in node_name.lower():
                is_autonomous_merge = True

            if is_autonomous_merge:
                github_client.admin_merge_pull_request(pr_url)
                log_stage_advancement("reflect", "Reflect Phase Completed", f"PR {pr_url} successfully created and AUTONOMOUSLY MERGED. HTIL bypassed (Administrative or Spec-First HTIL Inversion).")
            else:
                log_stage_advancement("reflect", "Reflect Phase Completed", f"PR {pr_url} successfully created. Entering Observe phase under HARD HITL block.")

    @record_execution(stage="act")
    def retro_attach(self, retro_file: str, branch_name: str) -> str:
        """Attaches a retrospective file to the active node branch by staging, committing, and pushing it.

        Args:
            retro_file: Absolute or relative path to the retro-<id>.md file.
            branch_name: The active node branch (e.g. node/806-implement-...).

        Returns:
            The path that was committed.
        """
        log_stage_advancement("act", "Retro Attach", f"Attaching retrospective to branch '{branch_name}'")

        from drivers import path_resolver

        # Resolve repo root (works from root or inside a worktree)
        repo_root = path_resolver.get_workspace_dir()

        # Resolve the retro file to an absolute path
        if not os.path.isabs(retro_file):
            # Try relative to repo root first
            candidate = os.path.join(repo_root, retro_file)
            if os.path.exists(candidate):
                retro_file = candidate
            else:
                # Try CWD
                retro_file = os.path.abspath(retro_file)

        if not os.path.exists(retro_file):
            raise FileNotFoundError(
                f"Retro Attach Failed: retro file '{retro_file}' does not exist. "
                f"Create it first with the Agentic Retro Trigger."
            )

        # Validate the branch exists locally or on remote
        strip_prefix = branch_name.replace("node/", "", 1)
        worktree_path = self.get_worktree_path(branch_name)

        # Determine the correct cwd for git operations
        if os.path.isdir(worktree_path):
            git_cwd = worktree_path
        else:
            git_cwd = repo_root

        # Compute relative path of the retro file from the git_cwd
        try:
            rel_retro = os.path.relpath(retro_file, git_cwd)
        except ValueError:
            # On Windows cross-drive; fallback to absolute
            rel_retro = retro_file

        # Ensure the retro file is inside the repo tree
        retro_dest = os.path.join(git_cwd, "artifacts", "audit", os.path.basename(retro_file))
        if retro_file != retro_dest and not os.path.exists(retro_dest):
            import shutil
            os.makedirs(os.path.dirname(retro_dest), exist_ok=True)
            shutil.copy2(retro_file, retro_dest)
            retro_file = retro_dest

        rel_retro = os.path.relpath(retro_file, git_cwd)

        # Stage the file
        git_client.add([rel_retro], cwd=git_cwd)

        # Commit
        commit_msg = f"docs(retro): attach retrospective {os.path.basename(retro_file)} to node #{self.issue_id}"
        try:
            git_client.commit(commit_msg, cwd=git_cwd)
        except Exception as e:
            if "nothing to commit" in str(e).lower() or "nothing added" in str(e).lower():
                print(f"ℹ️  Retro file already committed on branch '{branch_name}'. Nothing to do.")
                return retro_file
            raise

        # Push
        git_client.push(branch_name, cwd=git_cwd)

        log_stage_advancement("act", "Retro Attached", f"Retrospective '{os.path.basename(retro_file)}' committed and pushed to '{branch_name}'.")
        return retro_file

    @classmethod
    def clean_if_merged(cls, branch_name: str):
        """Cleans up the local worktree and branch if it has been merged."""
        try:
            state = github_client.get_pr_state_by_branch(branch_name)
            if state not in ["MERGED", "CLOSED"]:
                print(f"Skipping clean for branch {branch_name} because its PR state on GitHub is {state}.")
                return
        except Exception as e:
            print(f"Warning: Failed to verify PR state on GitHub for branch {branch_name}: {e}")
            return

        workspace_dir = os.environ.get("SPAO_WORKSPACE_DIR")
        if workspace_dir:
            possible_paths = [
                os.path.join(os.path.abspath(workspace_dir), ".worktrees", branch_name)
            ]
        else:
            possible_paths = [
                os.path.join(".worktrees", branch_name),
                os.path.join(".worktrees", "spao", branch_name),
                os.path.join(".worktrees", "sdlc", branch_name),
            ]
        for wt_path in possible_paths:
            if os.path.exists(wt_path):
                git_client.worktree_remove(wt_path, force=True)
        git_client.branch_delete(branch_name)

    @record_execution(stage="cancel")
    def cancel(self, frontier_file: str, node_name: str, reason: str) -> None:
        from drivers import path_resolver
        if not os.path.isabs(frontier_file):
            frontier_file = path_resolver.resolve_workspace_path(frontier_file)

        with FlowTransaction(frontier_file) as tx:
            log_stage_advancement("cancel", "Initiating Cancel Phase", f"Closing Issue #{self.issue_id} and canceling node")
            
            self.close(f"Node canceled by Metasystem. Reason: {reason}")
            tx.register_rollback(self.reopen)
            
            # Automate Meta-Index Checkbox Synchronization
            active_path_str = agent_frontier.read_active_path(frontier_file)
            if active_path_str:
                path_issue_id = agent_frontier.extract_path_id(active_path_str)
                if path_issue_id:
                    from kernel import daemon_backlog
                    backlog = daemon_backlog.BacklogDaemon()
                    # Check off the node so it doesn't block the path
                    backlog.check_off_meta_index(path_issue_id, self.issue_id)
                    tx.register_rollback(backlog.uncheck_meta_index, path_issue_id, self.issue_id)
                else:
                    print(f"Warning: Failed to extract Path ID from active path string: '{active_path_str}'")
                    
            # ATOMIC UPDATE: Mark node cancelled AND clear pointers
            agent_frontier.cancel_active_node(frontier_file, node_name, reason, clear_pointers=True)
