import os
import re
import hashlib
import subprocess
from drivers import github_client, git_client
from kernel import agent_frontier
from kernel import daemon_testing
from kernel import daemon_prompt
from kernel.daemon_prompt import process_prompts, get_backlog_file, clean_prompts
from kernel.daemon_status import get_local_worktrees
from kernel.sense_hooks import HookDaemon

from kernel.node_lifecycle import TerminalNode, BaseNode, log_stage_advancement
from kernel.daemon_telemetry import TelemetryDaemon, record_execution

def is_verbose() -> bool:
    """Checks if verbose mode is triggered by the operator."""
    return os.environ.get("SPAO_VERBOSE") in ("1", "true", "TRUE") or os.environ.get("SPOA_VERBOSE") in ("1", "true", "TRUE")

def plan_start_node(issue_id: str) -> None:
    """Acquires the GH Issue label lock to begin a multi-phase planning sequence."""
    node = TerminalNode(issue_id)
    node.plan_start()

def plan_finish_node(issue_id: str, body: str) -> str:
    """Finalizes a multi-phase plan by committing the Node Contract into the existing Issue."""
    node = TerminalNode(issue_id)
    return node.plan_finish(body)

def checkout_node(issue_id: str, branch_name: str) -> None:
    """Creates a git worktree for a new node."""
    node = TerminalNode(issue_id)
    node.checkout(branch_name)

@record_execution(stage="sense")
def sync_and_clean_node() -> None:
    """Synchronizes local workspace state, pruning merged nodes and tracking ROM updates."""
    import os
    import sys
    import hashlib
    import subprocess
    import yaml
    from drivers import path_resolver
    from kernel.node_lifecycle import TerminalNode



    repo_root = path_resolver.get_workspace_dir()
    gemini_path = os.path.join(repo_root, "GEMINI.md")
    
    # 1. Read prompt backlog to determine if Remote Mode is triggered
    backlog_file = get_backlog_file()
    remote_mode = False
    pending_sluice_prompts = []
    
    if os.path.exists(backlog_file):
        try:
            with open(backlog_file, "r", encoding="utf-8") as f:
                backlog_data = yaml.safe_load(f) or {}
            for prompt in backlog_data.get("prompts", []):
                if prompt.get("status") == "pending" and str(prompt.get("text", "")).startswith("[NOTIFICATION] Sluice Gate Opened: PR for Node"):
                    remote_mode = True
                    pending_sluice_prompts.append(prompt)
        except Exception as e:
            print(f"Warning: Failed to parse prompt backlog: {e}")

    # 2. Remote Mode: fetch remote updates
    if remote_mode:
        print("Sluice Gate event pending. Running remote synchronization...")
        git_client.fetch("origin", prune=True)
    else:
        print("No Sluice Gate events pending. Running offline-by-default local synchronization...")

    git_client.switch("origin/main", detach=True)
    
    # 3. Assert WIP-N=1 Invariant
    if remote_mode:
        open_prs = github_client.get_open_prs()
        if open_prs:
            def format_pr(pr):
                import re
                branch = pr.get('headRefName', '')
                m = re.match(r'^node/(\d+)', branch)
                node_part = f" for Node #{m.group(1)}" if m else ""
                return f"PR #{pr['number']}{node_part} (branch: {branch})"
            
            pr_list = ", ".join([format_pr(pr) for pr in open_prs])
            raise Exception(f"WIP-N=1 Violation: Cannot initiate SENSE phase while PRs are still open: {pr_list}")
    else:
        open_worktrees = get_local_worktrees(repo_root)
        if open_worktrees:
            still_open = []
            for w in open_worktrees:
                branch = w.get('branch', w.get('url', '').replace('local:', ''))
                try:
                    state = github_client.get_pr_state_by_branch(branch)
                    if state in ["MERGED", "CLOSED"]:
                        print(f"Auto-pruning worktree for Node {w.get('number', '?')} as its remote PR is {state}.")
                        TerminalNode.clean_if_merged(branch)
                        continue
                except Exception as e:
                    print(f"Warning: Failed to fetch state for branch {branch}: {e}")
                still_open.append(w)
            
            if still_open:
                wt_list = ", ".join([f"Node #{w.get('number', '?')} (branch: {w.get('branch', w.get('url', ''))})" for w in still_open])
                raise Exception(f"WIP-N=1 Violation: Cannot initiate SENSE phase while local Node worktrees are still active: {wt_list}\n(If the corresponding PR was merged on GitHub, you must manually delete this worktree to sync offline.)")
    
    merged_branches = set()
    
    # 4. Local merged branches
    for branch in git_client.list_merged_branches():
        b = branch.strip()
        if b and b != 'main':
            merged_branches.add(b)
            
    # 5. Remote merged PRs (Remote Mode only)
    if remote_mode:
        try:
            merged_prs = github_client.get_merged_prs(limit=50)
            for pr in merged_prs:
                if pr.get("headRefName"):
                    merged_branches.add(pr["headRefName"])
        except Exception as e:
            print(f"Warning: Failed to fetch merged PRs from GitHub: {e}")
 
    # Verify which of these actually exist locally and clean them
    local_branches = set(git_client.list_local_branches())
    
    for branch in merged_branches:
        if branch in local_branches and branch != 'main':
            TerminalNode.clean_if_merged(branch)
            
    git_client.worktree_prune()

    # 6. Consume Sluice Gate Opened prompts
    if remote_mode and pending_sluice_prompts:
        prompt_ids = ",".join([p["id"] for p in pending_sluice_prompts])
        process_prompts(prompt_ids, resolution_context="sync")
        clean_prompts()
 
    # 7. Automate standalone backlog mapping and quarantine status label cleanup
    try:
        import re
        from kernel.daemon_backlog import BacklogDaemon
        backlog_daemon = BacklogDaemon()
        open_issues = github_client.get_open_issues()
        
        # A. Find or create the Triage Holding Path
        triage_path_id = None
        triage_path = None
        for issue in open_issues:
            title_lower = issue.get("title", "").lower()
            labels = [l.get("name").lower() for l in issue.get("labels", []) if isinstance(l, dict) and "name" in l]
            labels += [l.lower() for l in issue.get("labels", []) if isinstance(l, str)]
            if "path" in labels and "triage holding" in title_lower:
                triage_path_id = str(issue["number"])
                triage_path = issue
                break
                
        if not triage_path_id:
            try:
                print("Triage Holding Path not found. Autonomously creating it...")
                url = backlog_daemon.add(
                    node_type="path",
                    title="Triage Holding - Standalone Triage & External Requirement Intakes",
                    goal="A holding Path to consolidate all unpromoted status:triage external intake nodes under the same parent class."
                )
                triage_path_id = url.split("/")[-1]
                # Refetch open issues to include the new path
                open_issues = github_client.get_open_issues()
                for issue in open_issues:
                    if str(issue["number"]) == triage_path_id:
                        triage_path = issue
                        break
            except Exception as ex:
                print(f"Warning: Failed to create Triage Holding Path: {ex}")

        # B. Clean up quarantine status labels for any issue with the backlog label
        for issue in open_issues:
            issue_id = str(issue["number"])
            labels = [l.get("name") for l in issue.get("labels", []) if isinstance(l, dict) and "name" in l]
            labels += [l for l in issue.get("labels", []) if isinstance(l, str)]
            
            labels_lower = [l.lower() for l in labels]
            if "backlog" in labels_lower:
                for l in labels:
                    if l.lower() in ["status:triage", "triage", "status:intake", "intake"]:
                        try:
                            github_client.remove_label(issue_id, l)
                            print(f"Automatically removed quarantine label '{l}' from Node #{issue_id}.")
                        except Exception as ex:
                            print(f"Warning: Failed to clean label '{l}' on Node #{issue_id}: {ex}")

        # C. Re-fetch open issues to have consistent labels, then process triage and mapping
        open_issues = github_client.get_open_issues()
        if triage_path_id:
            # Update triage_path to the latest fetched state
            for issue in open_issues:
                if str(issue["number"]) == triage_path_id:
                    triage_path = issue
                    break

        # D. Map unpromoted status:triage terminal nodes to Triage Holding Path
        triage_path_body = triage_path.get("body") or "" if triage_path else ""
        triage_body_changed = False
        
        for issue in open_issues:
            issue_id = str(issue["number"])
            if issue_id == triage_path_id:
                continue
            labels = [l.get("name").lower() for l in issue.get("labels", []) if isinstance(l, dict) and "name" in l]
            labels += [l.lower() for l in issue.get("labels", []) if isinstance(l, str)]
            
            # Quarantined node: has status:triage (or triage) and NOT backlog
            is_quarantined = ("status:triage" in labels or "triage" in labels) and "backlog" not in labels
            title = issue.get("title", "")
            is_terminal = any(t in title.lower() for t in ["activity", "discovery", "intake"])
            
            if is_terminal:
                checkbox_pattern = re.compile(r"-\s+\[[\s*xX]\]\s+Node\s+" + issue_id + r":", re.IGNORECASE)
                has_checkbox = checkbox_pattern.search(triage_path_body)
                
                if is_quarantined:
                    # Ensure it is in the Triage Holding Path's Meta-Index
                    if not has_checkbox:
                        checkbox_line = f"- [ ] Node {issue_id}: {title}"
                        if "## Meta-Index" in triage_path_body:
                            triage_path_body += f"\n{checkbox_line}"
                        else:
                            triage_path_body += f"\n\n## Meta-Index\n{checkbox_line}"
                        triage_body_changed = True
                        print(f"Automatically grouped quarantined Node #{issue_id} under Triage Holding Path.")
                else:
                    # Promoted or non-triage node: remove from Triage Holding Path if present
                    if has_checkbox:
                        # Strip the checkbox line completely
                        line_pattern = re.compile(r"-\s+\[[\s*xX]\]\s+Node\s+" + issue_id + r":[^\n]*\n?", re.IGNORECASE)
                        triage_path_body = line_pattern.sub("", triage_path_body)
                        triage_body_changed = True
                        print(f"Pruned promoted/active Node #{issue_id} from Triage Holding Path.")
                        
        if triage_body_changed and triage_path_id:
            try:
                github_client.update_issue_body(triage_path_id, triage_path_body)
            except Exception as ex:
                print(f"Warning: Failed to update Triage Holding Path body: {ex}")

        # E. Automate parent path mapping for standalone backlog terminal nodes
        paths = []
        mapped_nodes = set()
        for issue in open_issues:
            labels = [l.get("name").lower() for l in issue.get("labels", []) if isinstance(l, dict) and "name" in l]
            labels += [l.lower() for l in issue.get("labels", []) if isinstance(l, str)]
            if "path" in labels:
                paths.append(issue)
                body = issue.get("body") or ""
                node_ids = re.findall(r"-\s+\[[\s*xX]\]\s+Node\s+(\d+):", body)
                for nid in node_ids:
                    mapped_nodes.add(str(nid))
                    
        terminal_backlog_nodes = []
        for issue in open_issues:
            issue_id = str(issue["number"])
            if issue_id == triage_path_id:
                continue
            labels = [l.get("name").lower() for l in issue.get("labels", []) if isinstance(l, dict) and "name" in l]
            labels += [l.lower() for l in issue.get("labels", []) if isinstance(l, str)]
            if "backlog" in labels and "path" not in labels:
                title = issue.get("title", "")
                is_terminal = any(t in title.lower() for t in ["activity", "discovery", "intake"])
                if is_terminal and issue_id not in mapped_nodes:
                    terminal_backlog_nodes.append(issue)
                    
        if terminal_backlog_nodes:
            print(f"Found {len(terminal_backlog_nodes)} standalone backlog terminal nodes to map automatically.")
            for node in terminal_backlog_nodes:
                node_id = str(node["number"])
                node_title = node["title"]
                node_body = node.get("body") or ""
                best_path = None
                
                # Method A: Explicit Path ID reference
                path_matches = re.findall(r"path\s*#?(\d+)", node_body + " " + node_title, re.IGNORECASE)
                for pm in path_matches:
                    for path in paths:
                        if str(path["number"]) == pm:
                            best_path = path
                            break
                    if best_path:
                        break
                        
                # Method B: Keyword overlap
                if not best_path and paths:
                    node_words = set(re.findall(r"\w+", node_title.lower()))
                    stop_words = {"intake", "activity", "discovery", "and", "or", "the", "a", "of", "to", "for", "in", "on", "with", "at", "by", "from"}
                    node_words = node_words - stop_words
                    best_score = 0
                    for path in paths:
                        if str(path["number"]) == triage_path_id:
                            continue
                        path_title = path["title"]
                        path_words = set(re.findall(r"\w+", path_title.lower())) - stop_words
                        overlap = len(node_words.intersection(path_words))
                        if overlap > best_score:
                            best_score = overlap
                            best_path = path
                            
                # Method C: Fall back to first open Path (excluding triage holding path)
                if not best_path and paths:
                    for path in paths:
                        if str(path["number"]) != triage_path_id:
                            best_path = path
                            break
                    
                if best_path:
                    path_id = str(best_path["number"])
                    path_body = best_path.get("body") or ""
                    checkbox_line = f"- [ ] Node {node_id}: {node_title}"
                    if "## Meta-Index" in path_body:
                        path_body += f"\n{checkbox_line}"
                    else:
                        path_body += f"\n\n## Meta-Index\n{checkbox_line}"
                    try:
                        github_client.update_issue_body(path_id, path_body)
                        print(f"Automatically mapped Node #{node_id} ('{node_title}') to parent Path #{path_id} ('{best_path['title']}').")
                    except Exception as ex:
                        print(f"Error: Failed to map Node #{node_id} to Path #{path_id}: {ex}")
    except Exception as ex:
        print(f"Warning: Failed to execute automated backlog mapping/cleanup: {ex}")

    log_stage_advancement("sense", "Sense Phase Completed", "Workspace successfully synchronized and pruned.")
 
    # Trigger Metasystem Audit
    print("\n🔍 Executing Metasystem Integrity Audit...")
    audit_script = path_resolver.resolve_core_path("drivers", "audit_daemon.py")
    audit_cmd = [sys.executable, audit_script]
    if not remote_mode:
        audit_cmd.append("--local")
    subprocess.run(audit_cmd, check=False)
 
    # Surface pending backlog items at Sense phase
    daemon = HookDaemon()
    daemon.execute_all(local_mode=not remote_mode)

def reflect_node(frontier_file: str, issue_id: str, node_name: str, learnings: str, invariants: list[str], commit_msg: str, branch_name: str, stage: str = "all", insights: str = "") -> None:
    """Closes the GH issue, creates a PR, and updates the frontier."""
    node = TerminalNode(issue_id)
    node.reflect(frontier_file, node_name, learnings, invariants, commit_msg, branch_name, stage=stage, insights=insights)


import argparse
import sys
import json

def cmd_sync(args):
    sync_and_clean_node()

def cmd_plan_start(args):
    plan_start_node(args.issue_id)

def cmd_plan_finish(args):
    print(plan_finish_node(args.issue_id, args.body_content))

def cmd_checkout(args):
    checkout_node(args.issue_id, args.branch_name)

def cmd_reflect(args):
    if args.invariants.startswith("[") and args.invariants.endswith("]"):
        invariants = json.loads(args.invariants)
    else:
        invariants = [inv.strip() for inv in args.invariants.split(",") if inv.strip()]
        
    reflect_node(
        frontier_file=args.frontier_file,
        issue_id=args.issue_id,
        node_name=args.node_name,
        learnings=args.learnings,
        invariants=invariants,
        commit_msg=args.commit_msg,
        branch_name=args.branch_name,
        stage=args.stage,
        insights=args.insights
    )

def cancel_node(frontier_file: str, issue_id: str, node_name: str, reason: str) -> None:
    """Closes the GH issue, updates frontier to cancelled."""
    from kernel.node_lifecycle import TerminalNode
    node = TerminalNode(issue_id)
    node.cancel(frontier_file, node_name, reason)

def cmd_cancel(args):
    cancel_node(
        frontier_file=args.frontier_file,
        issue_id=args.issue_id,
        node_name=args.node_name,
        reason=args.reason
    )

def cmd_view(args):
    import re
    from drivers import gh_graph_skill
    
    data = github_client.get_issue_details(args.issue_id)
    print('='*40)
    print(f"Issue #{args.issue_id}: {data['title']} [{data['state']}]")
    print('='*40)
    
    body = data.get('body', '')
    
    if "## Meta-Index" in body:
        parts = body.split("## Meta-Index")
        pre_meta = parts[0]
        meta_section = parts[1]
        
        meta_parts = re.split(r'\n## ', meta_section, maxsplit=1)
        meta_text = meta_parts[0]
        post_meta = "\n## " + meta_parts[1] if len(meta_parts) > 1 else ""
        
        try:
            nodes = gh_graph_skill.parse_meta_index(meta_text)
            ready_nodes = set(gh_graph_skill.get_ready_nodes(nodes))
            
            rendered_lines = ["## Meta-Index"]
            
            roots = [nid for nid, ndata in nodes.items() if not ndata["depends"]]
            roots.sort(key=int)
            
            visited = set()
            
            def render_node(nid, prefix, is_last, is_root):
                if nid not in nodes:
                    return
                ndata = nodes[nid]
                
                if ndata["completed"]:
                    status_str = "[x]"
                elif nid in ready_nodes:
                    status_str = "[Ready]"
                else:
                    status_str = "[Blocked]"
                
                dep_str = ""
                if ndata["depends"]:
                    dep_str = f" [Depends: {', '.join(ndata['depends'])}]"
                
                # Check visited before printing to prevent duplicate printing
                if nid in visited:
                    if not is_root:
                        connector = "└──► " if is_last else "├──► "
                        rendered_lines.append(f"{prefix}{connector}{status_str} Node {nid} (Already rendered above)")
                    return
                visited.add(nid)
                    
                if is_root:
                    rendered_lines.append(f"{status_str} Node {nid}: {ndata['title']}")
                    new_prefix = ""
                else:
                    connector = "└──► " if is_last else "├──► "
                    rendered_lines.append(f"{prefix}{connector}{status_str} Node {nid}: {ndata['title']}{dep_str}")
                    new_prefix = prefix + ("    " if is_last else "│   ")
                
                children = [cid for cid, cdata in nodes.items() if nid in cdata["depends"]]
                children.sort(key=int)
                
                for i, child_id in enumerate(children):
                    render_node(child_id, new_prefix, i == len(children) - 1, False)
            
            for root in roots:
                render_node(root, "", True, True)
                
            print(pre_meta.strip())
            print("\n")
            print("\n".join(rendered_lines))
            print("\n")
            print(post_meta.strip() if post_meta.strip() != "##" else "")
            
        except Exception as e:
            # Fallback to raw body if parsing fails
            print(body)
    else:
        print(body)
        
    print('='*40)

def cmd_retro(args):
    import glob
    import os
    import sys
    from kernel.daemon_retro import RetroCompiler
    
    if args.retro_command == "compile":
        compiler = RetroCompiler(args.start_path, args.end_path)
        compiler.compile(args.output_path)
    elif args.retro_command == "list":
        files = glob.glob(os.path.join("artifacts", "retrospective_path_*.md"))
        if not files:
            print("No compiled retrospectives found.")
        else:
            print("\n📋 Compiled Retrospectives:")
            for f in sorted(files):
                basename = os.path.basename(f)
                print(f"  - {basename}")
            print()
    elif args.retro_command == "view":
        start = args.start_path
        end = args.end_path or start
        file_path = os.path.join("artifacts", f"retrospective_path_{start}_{end}.md")
        if not os.path.exists(file_path):
            print(f"Error: Retrospective file {file_path} not found.")
            sys.exit(1)
        with open(file_path, "r") as f:
            print(f.read())
    elif args.retro_command == "attach":
        node = TerminalNode(args.issue_id)
        node.retro_attach(args.retro_file, args.branch_name)

def cmd_set_status(args):
    node = BaseNode(args.issue_id)
    node.set_status(args.status_key)

def cmd_set_classification(args):
    node = BaseNode(args.issue_id)
    node.set_classification(args.classification_key)

def cmd_test(args):
    log_stage_advancement("act", "Executing TDD Test Harness Validation", f"Running pytest on target: {args.target}")
    daemon = daemon_testing.TestDaemon()
    exit_code = daemon.run([args.target] if args.target else [])
    sys.exit(exit_code)

def main():
    import argparse
    import sys
    import json
    import traceback
    import os

    try:
        parser = argparse.ArgumentParser(description="Antigravity Domain Kernel for Node Lifecycle Management")
        parser.add_argument("--workspace", action="store_true", help="Execute command under the active workspace context")
        subparsers = parser.add_subparsers(dest="subcommand", required=True)

        # sync
        subparsers.add_parser("sync", help="Sync main, prune branches, and surface backlog")

        # plan-start
        parser_ps = subparsers.add_parser("plan-start", help="Lock an issue to start multi-phase planning")
        parser_ps.add_argument("issue_id")

        # plan-finish
        parser_pf = subparsers.add_parser("plan-finish", help="Complete the plan phase by writing the Node Contract")
        parser_pf.add_argument("issue_id")
        parser_pf.add_argument("body_content")

        # checkout
        parser_co = subparsers.add_parser("checkout", help="Create a worktree for the Act phase")
        parser_co.add_argument("issue_id")
        parser_co.add_argument("branch_name")

        # reflect
        parser_r = subparsers.add_parser("reflect", help="Close node, push branch, open PR")
        parser_r.add_argument("issue_id")
        parser_r.add_argument("node_name")
        parser_r.add_argument("learnings")
        parser_r.add_argument("invariants")
        parser_r.add_argument("commit_msg")
        parser_r.add_argument("branch_name")
        parser_r.add_argument("frontier_file", nargs="?", default="artifacts/frontier_state.md")
        parser_r.add_argument("--stage", nargs="?", const="all", default="all", help="Granular files to stage: 'all' (default), 'none', or list.")
        parser_r.add_argument("--insights", default="", help="Active Insights (e.g., WHY-0071, WHY-0075)")

        # cancel
        parser_c = subparsers.add_parser("cancel", help="Cancel a structurally redundant node")
        parser_c.add_argument("issue_id")
        parser_c.add_argument("node_name")
        parser_c.add_argument("reason")
        parser_c.add_argument("frontier_file", nargs="?", default="artifacts/frontier_state.md")

        # view
        parser_v = subparsers.add_parser("view", help="View a Node issue")
        parser_v.add_argument("issue_id")

        # set-status
        parser_ss = subparsers.add_parser("set-status", help="Set the logical status of a node")
        parser_ss.add_argument("issue_id")
        parser_ss.add_argument("status_key")

        # set-classification
        parser_sc = subparsers.add_parser("set-classification", help="Set the logical classification of a node")
        parser_sc.add_argument("issue_id")
        parser_sc.add_argument("classification_key")

        # test
        parser_t = subparsers.add_parser("test", help="Execute test harness validation")
        parser_t.add_argument("target", nargs="?", default="tests/", help="Target directory or file for pytest")

        # retro
        parser_retro = subparsers.add_parser("retro", help="Compile, list, or view retrospectives")
        subparsers_retro = parser_retro.add_subparsers(dest="retro_command", required=True)

        # retro compile
        parser_rc = subparsers_retro.add_parser("compile", help="Compile a retrospective for a range of path IDs")
        parser_rc.add_argument("start_path", help="Starting path ID")
        parser_rc.add_argument("end_path", help="Ending path ID")
        parser_rc.add_argument("output_path", nargs="?", default=None, help="Optional output path")

        # retro list
        subparsers_retro.add_parser("list", help="List compiled retrospectives")

        # retro view
        parser_rv = subparsers_retro.add_parser("view", help="View a compiled retrospective")
        parser_rv.add_argument("start_path", help="Starting path ID")
        parser_rv.add_argument("end_path", nargs="?", default=None, help="Optional ending path ID")

        # retro attach
        parser_ra = subparsers_retro.add_parser("attach", help="Attach a retro file to the active node branch")
        parser_ra.add_argument("issue_id", help="The node issue ID (e.g. 806)")
        parser_ra.add_argument("retro_file", help="Path to the retro-<id>.md file to attach")
        parser_ra.add_argument("branch_name", help="The active node branch (e.g. node/806-implement-...)")

        args = parser.parse_args()

        if getattr(args, "workspace", False):
            if not os.environ.get("SPAO_WORKSPACE_DIR"):
                from drivers import path_resolver
                os.environ["SPAO_WORKSPACE_DIR"] = os.path.abspath(os.path.join(path_resolver.get_core_dir(), ".workspace"))

        if args.subcommand == "sync":
            cmd_sync(args)
        elif args.subcommand == "plan-start":
            cmd_plan_start(args)
        elif args.subcommand == "plan-finish":
            cmd_plan_finish(args)
        elif args.subcommand == "cancel":
            cmd_cancel(args)
        elif args.subcommand == "checkout":
            cmd_checkout(args)
        elif args.subcommand == "reflect":
            cmd_reflect(args)
        elif args.subcommand == "view":
            cmd_view(args)
        elif args.subcommand == "set-status":
            cmd_set_status(args)
        elif args.subcommand == "set-classification":
            cmd_set_classification(args)
        elif args.subcommand == "test":
            cmd_test(args)
        elif args.subcommand == "retro":
            cmd_retro(args)

    except Exception as e:
        subcommand = getattr(args, 'subcommand', 'unknown') if 'args' in locals() else 'unknown'
        persona = os.environ.get("SPAO_PERSONA_ID", "Unknown")
        tb_str = traceback.format_exc()
        
        body = f"## System Crash Report\n\n**Subcommand:** `{subcommand}`\n**Persona:** `{persona}`\n\n### Traceback\n```python\n{tb_str}\n```\n"
        
        try:
            from kernel.daemon_backlog import BacklogDaemon
            from kernel.daemon_telemetry import TelemetryDaemon
            from drivers import github_client
            
            # Using node_type "path" to bypass terminal node path_id requirement
            backlog_daemon = BacklogDaemon()
            issue_url = backlog_daemon.add(
                node_type="path",
                title=f"[BUG] Intake: System Crash in {subcommand}",
                goal=body
            )
            
            issue_id = issue_url.split("/")[-1]
            try:
                github_client.add_label(issue_id, "status:triage")
                github_client.add_label(issue_id, "bug")
            except Exception as label_err:
                print(f"Warning: Failed to add labels to bug report: {label_err}")
            
            telemetry = TelemetryDaemon()
            telemetry.record_event("ERROR", {
                "subcommand": subcommand,
                "error": str(e),
                "traceback": tb_str
            })
            
            print(f"\n[❌ CRASH] A system crash was intercepted during execution.")
            print(f"The exception has been caught and a bug report has been autonomously filed.")
            print(f"Bug Report URL: {issue_url}\n")
            sys.exit(1)
            
        except Exception as reporting_error:
            print(f"\n[❌ CRASH] A system crash occurred: {e}")
            print(f"WARNING: The autonomous bug reporting mechanism also failed: {reporting_error}")
            print(f"\nOriginal Traceback:\n{tb_str}\n")
            sys.exit(1)

if __name__ == "__main__":
    main()
