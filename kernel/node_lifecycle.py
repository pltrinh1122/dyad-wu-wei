import os
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
    if not is_verbose():
        return
    stage_colors = {
        "sense": "🔍 SENSE",
        "plan": "📋 PLAN",
        "act": "⚡ ACT",
        "observe": "👀 OBSERVE",
        "reflect": "💾 REFLECT"
    }
    stage_label = stage_colors.get(stage.lower(), stage.upper())
    
    print("\n" + "═"*60)
    print(f" 🔄 SPAO Loop Stage  ►  {stage_label}")
    print(f" 📌 Status           ►  {status}")
    if details:
        print(f" 📝 Details          ►  {details}")
    print("═"*60 + "\n")

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
                
            raise Exception(f"State Dissonance: Cannot proceed because Node '{current_active}' is already marked as active in {frontier_file}. Release the lock first.")

    def _validate_spao_purity(self, worktree_path: str | None = None):
        """Validates that a loop:spao branch only modifies policy/documentation paths."""
        from drivers import path_resolver
        config = path_resolver.load_antigravity_yml()
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
                raise Exception(f"Orthogonal Scope Violation: Node {self.issue_id} has an identical title footprint to Node {issue['number']}")
                
            if current_goal and current_goal == other_goal:
                raise Exception(f"Orthogonal Scope Violation: Node {self.issue_id} has an identical goal footprint to Node {issue['number']}")

    @record_execution(stage="plan")
    def plan_start(self, frontier_file: str = "artifacts/frontier_state.md") -> None:
        from drivers import path_resolver
        if not os.path.isabs(frontier_file):
            frontier_file = path_resolver.resolve_workspace_path(frontier_file)
        with FlowTransaction(frontier_file) as tx:
            self._verify_state_purity(frontier_file)
            
            open_prs = github_client.get_open_prs()
            if open_prs:
                pr_list = [pr.get('number', 'Unknown') for pr in open_prs]
                raise Exception(f"WIP-N=1 Invariant Violation: Cannot plan node #{self.issue_id} because there are open pull requests: {pr_list}. You must merge or close them first.")
            
            from kernel.daemon_strategic import verify_node_transition_allowed
            verify_node_transition_allowed(self.issue_id)
            
            in_progress_label = load_node_status_config().get("in_progress", "status: in-progress")
            if in_progress_label in self.gh_labels:
                raise Exception(f"Node #{self.issue_id} is already in progress by another thread!")
                
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
                                raise Exception(f"Dependency Violation: Node #{self.issue_id} depends on Node #{dep_id}, which is still open!")
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
                        raise Exception("SPEC file violation: A corresponding WHAT- specification file under kb/ (e.g. kb/WHAT-*.md) must be created and modified/added to finish the Plan phase.")
            except Exception as e:
                if "SPEC file violation" in str(e):
                    raise
        
        # Enforce static KB conflict checks (SG-0005)
        from kernel import daemon_knowledge_accrual
        from drivers import path_resolver
        daemon_knowledge_accrual.run_kb_check(repo_root=path_resolver.get_workspace_dir(), strict=True)
        
        prefix = f"Node {self.issue_id}:"
        if not current_title.startswith(prefix):
            new_title = f"{prefix} {current_title}"
            github_client.rename_issue_title(self.issue_id, new_title)
            
        self.update_body(body)
        
        issue_url = f"https://github.com/pltrinh1122/agent-antigravity/issues/{self.issue_id}"
        log_stage_advancement("plan", "Plan Phase Completed", f"Node issue #{self.issue_id} successfully planned. Transitioning to Act phase.")
        return issue_url

    @record_execution(stage="act")
    def checkout(self, branch_name: str, frontier_file: str = "artifacts/frontier_state.md") -> None:
        if not re.match(r"^node/\d+-[a-z0-9-]+$", branch_name):
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
                pr_list = [pr.get('number', 'Unknown') for pr in open_prs]
                raise Exception(f"WIP-N=1 Invariant Violation: Cannot checkout node #{self.issue_id} because there are open pull requests: {pr_list}. You must merge or close them first.")
            
            self.set_status("in_progress")
            tx.register_rollback(self.set_status, "open")
            
            worktree_path = self.get_worktree_path(branch_name)
            log_stage_advancement("act", "Initializing Execution Worktree", f"Creating git worktree at {worktree_path}")
            
            os.makedirs(os.path.dirname(worktree_path), exist_ok=True)
            
            git_client.fetch("origin")
            git_client.worktree_add(branch_name, worktree_path, "origin/main")
            tx.register_rollback(git_client.worktree_remove, worktree_path, force=True)
            tx.register_rollback(git_client.branch_delete, branch_name)
            
            print(f"\nWorktree established. Please `cd {worktree_path}` to begin work.")
    def reflect(self, frontier_file: str, node_name: str, learnings: str, invariants: list[str], commit_msg: str, branch_name: str, stage: str = "all", insights: str = "") -> None:
        if not re.match(r"^node/\d+-[a-z0-9-]+$", branch_name):
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

        with FlowTransaction(frontier_file) as tx:
            log_stage_advancement("reflect", "Initiating Reflect Phase", f"Closing Issue #{self.issue_id}, updating ledger, and preparing branch: '{branch_name}'")
            
            # Enforce Conflict-Free Reflection Invariant (WHY-0083)
            git_client.fetch("origin")
            if git_client.check_merge_conflicts("origin/main", cwd=worktree_dir):
                raise Exception(f"Reflection Blocked (WHY-0083): Branch '{branch_name}' has unresolved merge conflicts with 'origin/main'. You must resolve these conflicts locally before reflecting.")
            
            # Enforce post-failure reflection gate (SG-0005)
            from kernel import daemon_knowledge_accrual
            daemon_knowledge_accrual.enforce_reflection_hook(self.issue_id, repo_root=main_repo)
            
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
            
            # ATOMIC UPDATE: Mark node completed AND clear pointers
            agent_frontier.complete_active_node(frontier_file, node_name, learnings, invariants, clear_pointers=True)
            if clear_path:
                agent_frontier.set_active_path(frontier_file, "None")
            
            # Sync frontier state updates to worktree so they are committed in the branch
            try:
                import shutil
                for ext in [".yml", ".yml.sha256", ".md"]:
                    src = os.path.join(main_repo, "artifacts", f"frontier_state{ext}")
                    dest = os.path.join(worktree_dir, "artifacts", f"frontier_state{ext}")
                    if os.path.exists(src) and os.path.abspath(src) != os.path.abspath(dest):
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        shutil.copy2(src, dest)
            except Exception as e:
                print(f"Warning: Failed to sync frontier state files to worktree: {e}")
            
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

            # Rebase onto origin/main to ensure conflict-free push (Node 848)
            git_client.fetch("origin", cwd=worktree_dir)
            git_client.rebase("origin/main", cwd=worktree_dir)

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
            
            pr_url = github_client.create_pull_request(node_name, pr_body, head=branch_name)
            
            log_stage_advancement("reflect", "Reflect Phase Completed", f"PR successfully created. Entering Observe phase under HARD HITL block.")

    @classmethod
    def clean_if_merged(cls, branch_name: str):
        """Cleans up the local worktree and branch if it has been merged."""
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
