import os
import re
import subprocess
from skills import github_client
from skills import frontier_editor
from skills import testing_harness
from orchestrator import mgr_prompt

from orchestrator.node_lifecycle import TerminalNode, log_stage_advancement

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
            TerminalNode.clean_if_merged(b)
            
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
    node = TerminalNode(issue_id)
    node.reflect(frontier_file, node_name, learnings, invariants, commit_msg, branch_name, consumed_prompts)


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

def cmd_test(args):
    log_stage_advancement("act", "Executing TDD Test Harness Validation", f"Running pytest on target: {args.target}")
    exit_code = testing_harness.run_tests(args.target)
    sys.exit(exit_code)

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

    # test
    parser_t = subparsers.add_parser("test", help="Execute test harness validation")
    parser_t.add_argument("target", nargs="?", default="tests/", help="Target directory or file for pytest")

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
    elif args.subcommand == "test":
        cmd_test(args)

if __name__ == "__main__":
    main()
