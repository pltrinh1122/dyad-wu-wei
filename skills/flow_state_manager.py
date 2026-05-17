import re
import subprocess
from skills import github_client
from skills import frontier_editor

def plan_node(title: str, body: str) -> str:
    """Plans a node by creating a GH issue."""
    return github_client.create_issue(title, body)

def sync_and_clean_node() -> None:
    """Syncs main and prunes merged local branches."""
    subprocess.run(["git", "switch", "main"], check=True)
    subprocess.run(["git", "pull", "--prune", "origin", "main"], check=True)
    
    result = subprocess.run(["git", "branch", "--merged"], capture_output=True, text=True)
    branches = result.stdout.split('\n')
    for branch in branches:
        b = branch.strip().strip('* ')
        if b and b != 'main':
            # Don't check=True because branch -d can fail if it's not fully merged in git's eyes sometimes
            subprocess.run(["git", "branch", "-d", b])

def reflect_node(frontier_file: str, issue_id: str, node_name: str, learnings: str, invariants: list[str], commit_msg: str, branch_name: str, pr_title: str) -> None:
    """Closes the GH issue, creates a PR, and updates the frontier."""
    if not re.match(r"^node/\d+-[a-z0-9-]+$", branch_name):
        raise ValueError("Branch name MUST follow the standard: node/<id>-<kebab-case>")

    github_client.close_issue(issue_id, "Node completed via Flow-State Manager. Moving to PR.")
    
    frontier_editor.complete_active_node(frontier_file, node_name, learnings, invariants)
    
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)
    
    pr_body = f"Resolves #{issue_id}\n\n{learnings}"
    github_client.create_pull_request(pr_title, pr_body)
