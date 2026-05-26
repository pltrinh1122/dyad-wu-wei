import os
import re
import sys
import json
import yaml
import argparse
import subprocess
from kernel.daemon_telemetry import record_execution
from drivers import knowledge_accrual_skill

def get_repo_root():
    from drivers import path_resolver
    return path_resolver.get_workspace_dir()

def run_kb_check(repo_root: str, strict: bool = True) -> bool:
    """
    Executes a static conflict check on git changes within kb/ files against axioms.
    """
    import subprocess
    # Get staged and unstaged edits against HEAD
    res = subprocess.run(
        ["git", "diff", "HEAD"],
        capture_output=True,
        text=True,
        cwd=repo_root
    )
    if res.returncode != 0:
        res = subprocess.run(
            ["git", "diff"],
            capture_output=True,
            text=True,
            cwd=repo_root
        )

    diff_text = res.stdout
    conflicts = knowledge_accrual_skill.check_kb_conflicts(diff_text)

    if conflicts:
        print("❌ KB Conflict Check Failed:")
        for conflict in conflicts:
            print(f"  - {conflict}")
        if strict:
            raise Exception(f"KB Conflict Check Failed with {len(conflicts)} conflict(s). Blocked.")
        return False

    print("✅ KB Conflict Check Passed.")
    return True

def enforce_reflection_hook(issue_id: str, repo_root: str) -> None:
    """
    Scans telemetry events for errors on the current node. If errors are found,
    enforces the existence of a corresponding retrospective markdown file.
    """
    telemetry_file = os.path.join(repo_root, "artifacts", "telemetry.jsonl")
    has_failures = False
    has_positive_feedback = False

    if os.path.exists(telemetry_file):
        try:
            with open(telemetry_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    obj = json.loads(line)
                    # Support matching both string and int representation
                    node_val = obj.get("node_id")
                    if node_val and str(node_val).strip() == str(issue_id).strip():
                        event_type = str(obj.get("event", "")).upper()
                        status = obj.get("metadata", {}).get("status", "")
                        error = obj.get("metadata", {}).get("error", "")
                        if event_type == "FAILURE" or status == "error" or error:
                            has_failures = True
                        if event_type == "POSITIVE_FEEDBACK" or status == "positive_feedback":
                            has_positive_feedback = True
                        if has_failures and has_positive_feedback:
                            break
        except Exception as e:
            print(f"Warning: Failed to read telemetry file for reflection gate: {e}")

    if has_failures:
        retro_filename = f"retro-{issue_id}.md"
        retro_path = os.path.join(repo_root, "artifacts", "audit", retro_filename)
        if not os.path.exists(retro_path):
            raise Exception(
                f"REFLECTION BLOCKED: Node {issue_id} experienced execution failures. "
                f"Under SG-0005 (TG-0005-04), a structured post-mortem reflection record "
                f"is required under artifacts/audit/{retro_filename} before reflection."
            )
        print(f"✅ Post-failure reflection verified: {retro_filename} exists.")
        
        # Programmatic Retrospective Surfacing Check (Node 828)
        try:
            # Check if this retrospective has already been surfaced in the backlog (open or closed)
            chk_res = subprocess.run(
                ["gh", "issue", "list", "--state", "all", "--search", f"retro-{issue_id}", "--json", "number,title"],
                capture_output=True, text=True, check=True
            )
            matching = json.loads(chk_res.stdout.strip() or "[]")
            
            if not matching:
                print(f"🔍 Retrospective {retro_filename} has not been surfaced. Autonomously creating backlog activity...")
                
                from kernel import agent_frontier
                from drivers import github_client
                
                # Find parent path ID
                parent_path_id = None
                
                # 1. Sequential frontier lookup
                frontier_yml_path = os.path.join(repo_root, "artifacts", "frontier_state.yml")
                if os.path.exists(frontier_yml_path):
                    with open(frontier_yml_path, "r", encoding="utf-8") as f:
                        state_data = yaml.safe_load(f) or {}
                    nodes = state_data.get("nodes", [])
                    current_path_id = None
                    for node in nodes:
                        name = node.get("name", "")
                        if "path" in name.lower():
                            match = re.search(r"\bPath\s+(\d+)\b", name, re.IGNORECASE)
                            if match:
                                current_path_id = match.group(1)
                        match_node = re.search(r"\b(?:Node|Activity|Probe|Path)\s+(\d+)\b", name, re.IGNORECASE)
                        if match_node and str(match_node.group(1)) == str(issue_id):
                            if current_path_id:
                                parent_path_id = str(current_path_id)
                                break
                                
                # 2. GitHub checklist lookup
                if not parent_path_id:
                    path_issues = github_client.list_issues_by_label("path")
                    for path_issue in path_issues:
                        body = path_issue.get("body", "")
                        if f"#{issue_id}" in body or f"Node {issue_id}:" in body:
                            parent_path_id = str(path_issue["number"])
                            break
                            
                # 3. Fallback to active path
                if not parent_path_id:
                    if os.path.exists(frontier_yml_path):
                        with open(frontier_yml_path, "r", encoding="utf-8") as f:
                            state_data = yaml.safe_load(f) or {}
                        active_path_str = state_data.get("current_active_path")
                        if active_path_str:
                            parent_path_id = agent_frontier.extract_path_id(active_path_str)
                            
                if not parent_path_id:
                    print(f"Warning: Could not resolve parent Path ID for Node {issue_id}. Epistemic retro surfacing skipped.")
                else:
                    from kernel.daemon_backlog import BacklogDaemon
                    backlog_daemon = BacklogDaemon()
                    new_title = f"Reflect - Synthesize Epistemic Retrospective {retro_filename}"
                    new_goal = f"Synthesize the epistemic learnings from the post-failure retrospective {retro_filename} into the system's operational guidelines (the Dao)."
                    backlog_daemon.add(
                        node_type="activity",
                        title=new_title,
                        goal=new_goal,
                        path_id=parent_path_id
                    )
                    print(f"✅ Surfaced retrospective in backlog for Path {parent_path_id}")
            else:
                print(f"✅ Retrospective {retro_filename} is already surfaced in issue #{matching[0]['number']}.")
        except Exception as e:
            print(f"Warning: Failed to surface retrospective: {e}")
    else:
        print("✅ No failure events detected. Skipping mandatory reflection check.")

    if has_positive_feedback:
        reaffirm_filename = f"reaffirm-{issue_id}.md"
        reaffirm_path = os.path.join(repo_root, "artifacts", "audit", reaffirm_filename)
        if not os.path.exists(reaffirm_path):
            raise Exception(
                f"REFLECTION BLOCKED: Node {issue_id} received positive Operator feedback. "
                f"Under SG-0005, a codified insight is required under artifacts/audit/{reaffirm_filename} "
                f"before reflection to reaffirm the Dao."
            )
        print(f"✅ Positive feedback reflection verified: {reaffirm_filename} exists.")

def inject_contextual_rules(repo_root: str) -> None:
    """
    Resolves the current active path, builds contextual prompt injection,
    and writes it to GEMINI.md.
    """
    frontier_yml_path = os.path.join(repo_root, "artifacts", "frontier_state.yml")
    active_path_str = None
    if os.path.exists(frontier_yml_path):
        try:
            with open(frontier_yml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            active_path_str = data.get("current_active_path")
        except Exception as e:
            print(f"Warning: Failed to read active path from frontier state: {e}")

    kb_dir = os.path.join(repo_root, "kb")
    injection = knowledge_accrual_skill.build_contextual_prompt_injection(active_path_str, kb_dir)

    gemini_path = os.path.join(repo_root, "GEMINI.md")
    if os.path.exists(gemini_path):
        with open(gemini_path, "r", encoding="utf-8") as f:
            content = f.read()

        start_tag = "<!-- CONTEXTUAL_ROM_INJECTION_START -->"
        end_tag = "<!-- CONTEXTUAL_ROM_INJECTION_END -->"

        if start_tag in content and end_tag in content:
            pattern = re.compile(rf"{start_tag}.*?{end_tag}", re.DOTALL)
            new_content = pattern.sub(injection, content)
        else:
            new_content = content.rstrip() + "\n\n" + injection + "\n"

        with open(gemini_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ GEMINI.md updated with contextual prompt injection.")
    else:
        print(f"Warning: GEMINI.md not found at {gemini_path}")

@record_execution(stage="act")
def main():
    parser = argparse.ArgumentParser(description="Autonomous Knowledge Accrual Daemon")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # check-kb subcommand
    parser_check = subparsers.add_parser("check-kb", help="Run static KB conflict checking on git diff")
    parser_check.add_argument("--lax", action="store_true", help="Run in warning mode (do not raise error)")

    # enforce-retro subcommand
    parser_retro = subparsers.add_parser("enforce-retro", help="Verify retro post-failure file exists")
    parser_retro.add_argument("issue_id", help="Target node issue ID")

    # inject-context subcommand
    parser_inject = subparsers.add_parser("inject-context", help="Inject active path guidelines to GEMINI.md")

    # reaffirm subcommand — records positive Operator feedback and materialises the reaffirm document
    parser_reaffirm = subparsers.add_parser(
        "reaffirm",
        help="Record positive Operator feedback for a node, emitting a POSITIVE_FEEDBACK telemetry event and creating artifacts/audit/reaffirm-<id>.md",
    )
    parser_reaffirm.add_argument("issue_id", help="Target node issue ID")
    parser_reaffirm.add_argument(
        "insight",
        help="Description of the positive pattern to reaffirm into the Dao",
    )

    args = parser.parse_args()
    repo_root = get_repo_root()

    if args.command == "check-kb":
        run_kb_check(repo_root, strict=not args.lax)
    elif args.command == "enforce-retro":
        enforce_reflection_hook(args.issue_id, repo_root)
    elif args.command == "inject-context":
        inject_contextual_rules(repo_root)
    elif args.command == "reaffirm":
        reaffirm_path = os.path.join(repo_root, "artifacts", "audit", f"reaffirm-{args.issue_id}.md")
        knowledge_accrual_skill.record_positive_feedback(
            issue_id=args.issue_id,
            insight=args.insight,
            reaffirm_path=reaffirm_path,
        )
        print(f"✅ Positive feedback recorded for Node {args.issue_id}.")
        print(f"   Reaffirmation document: {reaffirm_path}")
        print(f"   POSITIVE_FEEDBACK telemetry event emitted.")

if __name__ == "__main__":
    main()

