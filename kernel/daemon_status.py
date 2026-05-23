import os
import sys
import yaml
import re

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from drivers.frontier_editor import read_active_path, read_active_node
from drivers.git_client import get_current_branch

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

def get_local_worktrees(repo_root: str) -> list[dict]:
    worktrees_dir = os.path.join(repo_root, ".worktrees")
    if not os.path.exists(worktrees_dir):
        return []
    
    prs = []
    
    def process_directory(path: str, category: str):
        try:
            for entry in os.listdir(path):
                entry_path = os.path.join(path, entry)
                if os.path.isdir(entry_path):
                    git_file = os.path.join(entry_path, ".git")
                    if os.path.exists(git_file) and os.path.isfile(git_file):
                        # Extract issue number
                        match = re.match(r"^(\d+)", entry)
                        issue_num_str = match.group(1) if match else ""
                        
                        # Format title
                        title = entry
                        if issue_num_str:
                            title = entry[len(issue_num_str):].lstrip("-")
                        title_clean = title.replace("-", " ").strip()
                        if title_clean:
                            title_clean = title_clean[0].upper() + title_clean[1:]
                        else:
                            title_clean = "Unknown Title"
                        
                        issue_num = int(issue_num_str) if issue_num_str else "?"
                        
                        if category:
                            branch_name = f"{category}/{entry}"
                        else:
                            branch_name = entry
                            
                        prs.append({
                            "number": issue_num,
                            "title": title_clean,
                            "url": f"local:{branch_name}"
                        })
        except Exception:
            pass

    # Scan specific subdirectories: node/, sdlc/, spao/
    for category in ["node", "sdlc", "spao"]:
        cat_dir = os.path.join(worktrees_dir, category)
        if os.path.exists(cat_dir):
            process_directory(cat_dir, category)
            
    # Scan root of .worktrees/ for any directly placed worktrees (excluding category dirs)
    try:
        for entry in os.listdir(worktrees_dir):
            if entry in ["node", "sdlc", "spao"]:
                continue
            entry_path = os.path.join(worktrees_dir, entry)
            if os.path.isdir(entry_path):
                git_file = os.path.join(entry_path, ".git")
                if os.path.exists(git_file) and os.path.isfile(git_file):
                    # This is a worktree directly under .worktrees/
                    match = re.match(r"^(\d+)", entry)
                    issue_num_str = match.group(1) if match else ""
                    
                    title = entry
                    if issue_num_str:
                        title = entry[len(issue_num_str):].lstrip("-")
                    title_clean = title.replace("-", " ").strip()
                    if title_clean:
                        title_clean = title_clean[0].upper() + title_clean[1:]
                    else:
                        title_clean = "Unknown Title"
                    
                    issue_num = int(issue_num_str) if issue_num_str else "?"
                    prs.append({
                        "number": issue_num,
                        "title": title_clean,
                        "url": f"local:{entry}"
                    })
    except Exception:
        pass
        
    def sort_key(pr):
        num = pr.get("number")
        if isinstance(num, int):
            return num
        return 999999
        
    prs.sort(key=sort_key)
    return prs

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
        
    open_prs = get_local_worktrees(repo_root)
    pr_count = len(open_prs)
        
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
