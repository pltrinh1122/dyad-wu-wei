import os
import sys
import yaml

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from drivers.frontier_editor import read_active_path, read_active_node
from drivers.git_client import get_current_branch
from drivers.github_client import get_open_prs

def get_prompt_backlog_size(repo_root: str) -> int:
    path = os.path.join(repo_root, "artifacts", "prompt_backlog.yml")
    if not os.path.exists(path):
        return 0
    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f) or {}
        return len(data.get("prompts", []))
    except Exception:
        return 0

def main():
    frontier_path = os.path.join(repo_root, "artifacts", "frontier_state.md")
    
    active_path = "None"
    active_node = "None"
    if os.path.exists(frontier_path):
        try:
            active_path = read_active_path(frontier_path) or "None"
        except Exception:
            pass
        try:
            active_node = read_active_node(frontier_path) or "None"
        except Exception:
            pass

    try:
        branch = get_current_branch(cwd=repo_root)
    except Exception:
        branch = "Unknown"
        
    try:
        open_prs = get_open_prs("origin/main")
        pr_count = len(open_prs)
    except Exception:
        open_prs = []
        pr_count = 0
        
    backlog_size = get_prompt_backlog_size(repo_root)

    print("=== Antigravity System Status ===")
    print(f"Active Path : {active_path}")
    print(f"Active Node : {active_node}")
    print(f"WIP Branch  : {branch}")
    print(f"Open PRs    : {pr_count}")
    if pr_count > 0:
        for pr in open_prs:
            print(f"  - #{pr.get('number', '?')}: {pr.get('title', 'Unknown')} ({pr.get('url', '')})")
    print(f"Prompt Queue: {backlog_size} item(s)")

if __name__ == "__main__":
    main()
