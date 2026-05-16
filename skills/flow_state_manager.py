import subprocess
from skills import github_client
from skills import frontier_editor

def plan_node(title: str, body: str) -> str:
    """Plans a node by creating a GH issue."""
    return github_client.create_issue(title, body)

def reflect_node(frontier_file: str, issue_id: str, node_name: str, learnings: str, invariants: list[str], commit_msg: str) -> None:
    """Closes the GH issue, updates the frontier, and pushes git."""
    github_client.close_issue(issue_id, "Node completed via Flow-State Manager.")
    
    frontier_editor.complete_active_node(frontier_file, node_name, learnings, invariants)
    
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
