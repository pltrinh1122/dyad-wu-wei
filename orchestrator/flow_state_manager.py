import os
import re
import subprocess
from skills import github_client
from skills import frontier_editor
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
