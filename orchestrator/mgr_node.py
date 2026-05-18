import os
import re
import subprocess
from skills import github_client
from skills import frontier_editor
from orchestrator import mgr_prompt

def is_verbose() -> bool:
    """Checks if verbose mode is triggered by the operator."""
    return os.environ.get("SPAO_VERBOSE") in ("1", "true", "TRUE") or os.environ.get("SPOA_VERBOSE") in ("1", "true", "TRUE")

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

def plan_start_node(issue_id: str) -> None:
    """Acquires the GH Issue label lock to begin a multi-phase planning sequence."""
    labels = github_client.get_issue_labels(issue_id)
    if "status: in-progress" in labels:
        raise Exception(f"Node #{issue_id} is already in progress by another thread!")
        
    github_client.add_label(issue_id, "status: in-progress")
    log_stage_advancement("plan", "Plan-Start Executed", f"Acquired lock on Node #{issue_id} for multi-phase planning.")

def plan_finish_node(issue_id: str, body: str) -> str:
    """Finalizes a multi-phase plan by committing the Node Contract into the existing Issue."""
    log_stage_advancement("plan", "Formulating Implementation Contract", f"Locking Node Contract into Issue #{issue_id}")
    
    import json
    # Retrieve current title to check if we need to rename it
    res = subprocess.run(["gh", "issue", "view", str(issue_id), "--json", "title"], capture_output=True, text=True, check=True)
    current_title = json.loads(res.stdout)["title"]
    
    prefix = f"Node {issue_id}:"
    if not current_title.startswith(prefix):
        new_title = f"{prefix} {current_title}"
        github_client.rename_issue_title(issue_id, new_title)
        
    github_client.update_issue_body(issue_id, body)
    
    issue_url = f"https://github.com/pltrinh1122/agent-antigravity/issues/{issue_id}"
    log_stage_advancement("plan", "Plan Phase Completed", f"Node issue #{issue_id} successfully planned. Transitioning to Act phase.")
    return issue_url

def checkout_node(issue_id: str, branch_name: str) -> None:
    """Creates a git worktree for a new node."""
    if not re.match(r"^node/\d+-[a-z0-9-]+$", branch_name):
        raise ValueError("Branch name MUST follow the standard: node/<id>-<kebab-case>")
        
    # The lock is expected to be acquired during plan-start.
    # However, to be resilient for legacy/hotfix operations, we can idempotently apply it.
    github_client.add_label(issue_id, "status: in-progress")
            
    log_stage_advancement("act", "Initializing Execution Worktree", f"Creating git worktree at .worktrees/{branch_name}")
    
    worktree_path = os.path.join(".worktrees", branch_name)
    os.makedirs(os.path.dirname(worktree_path), exist_ok=True)
    
    subprocess.run(["git", "worktree", "add", "-b", branch_name, worktree_path, "main"], check=True)
    
    print(f"\nWorktree established. Please `cd {worktree_path}` to begin work.")

def sync_and_clean_node() -> None:
    """Syncs main, prunes merged local branches, and surfaces pending backlog items."""
    log_stage_advancement("sense", "Initiating Sense Phase", "Syncing main, cleaning up local branches, and refreshing backlog state.")
    
    open_prs = github_client.get_open_prs()
    if open_prs:
        pr_list = ", ".join([f"#{pr['number']} ({pr['headRefName']})" for pr in open_prs])
        raise Exception(f"WIP-N=1 Violation: Cannot initiate SENSE phase while PRs are still open: {pr_list}")
        
    subprocess.run(["git", "switch", "main"], check=True)
    subprocess.run(["git", "pull", "--prune", "origin", "main"], check=True)
    
    result = subprocess.run(["git", "branch", "--merged"], capture_output=True, text=True)
    branches = result.stdout.split('\n')
    for branch in branches:
        b = branch.strip().strip('* ')
        if b and b != 'main':
            wt_path = os.path.join(".worktrees", b)
            if os.path.exists(wt_path):
                subprocess.run(["git", "worktree", "remove", "-f", wt_path])
            # Don't check=True because branch -d can fail if it's not fully merged in git's eyes sometimes
            subprocess.run(["git", "branch", "-d", b])
            
    subprocess.run(["git", "worktree", "prune"], check=False)

    log_stage_advancement("sense", "Sense Phase Completed", "Workspace successfully synchronized and pruned.")

    # Surface pending backlog items at Sense phase
    backlog_items = github_client.list_issues_by_label("backlog")
    if backlog_items:
        print(f"\n📋 Backlog ({len(backlog_items)} item(s) pending):")
        for item in backlog_items:
            print(f"  {item['title']}")
        print()

def reflect_node(frontier_file: str, issue_id: str, node_name: str, learnings: str, invariants: list[str], commit_msg: str, branch_name: str, consumed_prompts: str = None) -> None:
    """Closes the GH issue, creates a PR, updates the frontier, and consumes any prompts."""
    if not re.match(r"^node/\d+-[a-z0-9-]+$", branch_name):
        raise ValueError("Branch name MUST follow the standard: node/<id>-<kebab-case>")

    log_stage_advancement("reflect", "Initiating Reflect Phase", f"Closing Issue #{issue_id}, updating ledger, and preparing branch: '{branch_name}'")

    github_client.close_issue(issue_id, "Node completed via Flow-State Manager. Moving to PR.")
    
    frontier_editor.complete_active_node(frontier_file, node_name, learnings, invariants)
    
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)
    
    pr_body = f"Resolves #{issue_id}\n\n{learnings}"
    
    prompt_ids = []
    if consumed_prompts:
        prompt_ids = [p.strip() for p in consumed_prompts.split(",") if p.strip()]
        if prompt_ids:
            pr_body += "\n\n### Addresses Prompts\n"
            backlog_file = mgr_prompt.get_backlog_file()
            data = mgr_prompt.load_data(backlog_file)
            for p in data.get("prompts", []):
                if p["id"] in prompt_ids:
                    pr_body += f"- **{p['id']}**: {p['text']}\n"
                    
    pr_url = github_client.create_pull_request(node_name, pr_body)
    
    if prompt_ids:
        mgr_prompt.consume_prompts(",".join(prompt_ids), pr_url)
        backlog_file = mgr_prompt.get_backlog_file()
        subprocess.run(["git", "add", backlog_file], check=True)
        subprocess.run(["git", "commit", "-m", "chore: consume prompts"], check=True)
        subprocess.run(["git", "push", "origin", branch_name], check=True)


    log_stage_advancement("reflect", "Reflect Phase Completed", f"PR successfully created. Entering Observe phase under HARD HITL block.")


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
        consumed_prompts=args.prompts
    )

def cmd_view(args):
    res = subprocess.run(['gh', 'issue', 'view', args.issue_id, '--json', 'title,state,body'], capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    print('='*40)
    print(f"Issue #{args.issue_id}: {data['title']} [{data['state']}]")
    print('='*40)
    print(data['body'])
    print('='*40)

def main():
    parser = argparse.ArgumentParser(description="Antigravity Domain Orchestrator for Node Lifecycle Management")
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
    parser_r.add_argument("prompts", nargs="?", default=None)

    # view
    parser_v = subparsers.add_parser("view", help="View a Node issue")
    parser_v.add_argument("issue_id")

    args = parser.parse_args()

    if args.subcommand == "sync":
        cmd_sync(args)
    elif args.subcommand == "plan-start":
        cmd_plan_start(args)
    elif args.subcommand == "plan-finish":
        cmd_plan_finish(args)
    elif args.subcommand == "checkout":
        cmd_checkout(args)
    elif args.subcommand == "reflect":
        cmd_reflect(args)
    elif args.subcommand == "view":
        cmd_view(args)

if __name__ == "__main__":
    main()
