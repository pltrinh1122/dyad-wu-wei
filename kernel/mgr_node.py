import os
import re
import subprocess
from drivers import github_client, git_client
from kernel import mgr_frontier
from kernel import mgr_testing
from kernel import mgr_prompt
from kernel.sense_hooks import HookManager

from kernel.node_lifecycle import TerminalNode, BaseNode, log_stage_advancement
from kernel.mgr_telemetry import TelemetryManager, record_execution

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
    """Syncs main, prunes merged local branches, and surfaces pending backlog items."""
    log_stage_advancement("sense", "Initiating Sense Phase", "Syncing main, cleaning up local branches, and refreshing backlog state.")
    
    git_client.fetch("origin", prune=True)
    git_client.switch("origin/main", detach=True)

    open_prs = github_client.get_open_prs()
    if open_prs:
        pr_list = ", ".join([f"#{pr['number']} ({pr['headRefName']})" for pr in open_prs])
        raise Exception(f"WIP-N=1 Violation: Cannot initiate SENSE phase while PRs are still open: {pr_list}")
    
    merged_branches = set()
    
    # 1. Local merged branches
    for branch in git_client.list_merged_branches():
        b = branch.strip()
        if b and b != 'main':
            merged_branches.add(b)
            
    # 2. GitHub merged PRs
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
 
    log_stage_advancement("sense", "Sense Phase Completed", "Workspace successfully synchronized and pruned.")
 
    # Trigger Metasystem Audit
    print("\n🔍 Executing Metasystem Integrity Audit...")
    from drivers import path_resolver
    # Execute Metasystem Integrity Audit
    audit_script = path_resolver.resolve_core_path("drivers", "audit_daemon.py")
    subprocess.run([sys.executable, audit_script], check=False)
 
    # Surface pending backlog items at Sense phase
    manager = HookManager()
    manager.execute_all()

def reflect_node(frontier_file: str, issue_id: str, node_name: str, learnings: str, invariants: list[str], commit_msg: str, branch_name: str, stage: str = "all") -> None:
    """Closes the GH issue, creates a PR, and updates the frontier."""
    node = TerminalNode(issue_id)
    node.reflect(frontier_file, node_name, learnings, invariants, commit_msg, branch_name, stage=stage)


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
        stage=args.stage
    )

def cmd_view(args):
    data = github_client.get_issue_details(args.issue_id)
    print('='*40)
    print(f"Issue #{args.issue_id}: {data['title']} [{data['state']}]")
    print('='*40)
    print(data['body'])
    print('='*40)

def cmd_set_status(args):
    node = BaseNode(args.issue_id)
    node.set_status(args.status_key)

def cmd_set_classification(args):
    node = BaseNode(args.issue_id)
    node.set_classification(args.classification_key)

def cmd_test(args):
    log_stage_advancement("act", "Executing TDD Test Harness Validation", f"Running pytest on target: {args.target}")
    manager = mgr_testing.TestManager()
    exit_code = manager.run([args.target] if args.target else [])
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
    parser_r.add_argument("--stage", nargs="?", const="all", default="all", help="Granular files to stage: 'all' (default), 'none', or list.")

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
    elif args.subcommand == "set-status":
        cmd_set_status(args)
    elif args.subcommand == "set-classification":
        cmd_set_classification(args)
    elif args.subcommand == "test":
        cmd_test(args)

if __name__ == "__main__":
    main()
