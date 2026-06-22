from kernel.daemon_telemetry import record_execution
import os
import sys
import yaml
import re

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from drivers.git_client import get_current_branch

def get_prompt_backlog_size(repo_root: str) -> int:
    path = os.path.join(repo_root, "artifacts", "prompt_backlog.yml")
    if not os.path.exists(path):
        return 0
    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f) or {}
        prompts = data.get("prompts", [])
        return len([p for p in prompts if p.get("status") != "consumed"])
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

def print_goal_progress_report():
    """Calculates and prints progress bars for active strategic goals."""
    from kernel.daemon_strategic import load_ledger
    from drivers import github_client
    
    ledger = load_ledger()
    goals = ledger.get("strategic_goals", [])
    active_goals = [g for g in goals if g.get("status") == "Active"]
    if not active_goals:
        return
        
    print("\n--- Strategic Goal Progress ---")
    
    try:
        open_paths = github_client.list_issues_by_label("path")
    except Exception:
        open_paths = []
        
    open_paths_map = {}
    for issue in open_paths:
        open_paths_map[str(issue["number"])] = issue.get("title", f"Path {issue['number']}")
            
    for goal in active_goals:
        goal_id = goal.get("id")
        goal_title = goal.get("title")
        prioritized = goal.get("prioritized_paths", [])
        
        completed_count = 0
        total_count = len(prioritized)
        
        path_details = []
        for p_id in prioritized:
            p_id_str = str(p_id)
            if p_id_str not in open_paths_map:
                completed_count += 1
                try:
                    details = github_client.get_issue_details(p_id_str)
                    title = details.get("title", f"Path {p_id_str}")
                except Exception:
                    title = f"Path {p_id_str}"
                path_details.append((True, p_id_str, title))
            else:
                title = open_paths_map[p_id_str]
                path_details.append((False, p_id_str, title))
                
        if total_count == 0:
            percentage = 100.0
            filled = 10
        else:
            percentage = (completed_count / total_count) * 100.0
            filled = int(round(completed_count / total_count * 10))
            
        bar = "█" * filled + "░" * (10 - filled)
        
        print(f"🎯 [{goal_id}] {goal_title}")
        print(f"   [{bar}] {percentage:.1f}% ({completed_count}/{total_count})")
        for is_completed, p_id, title in path_details:
            mark = "x" if is_completed else " "
            clean_title = re.sub(r"^Path\s*\d+:\s*", "", title, flags=re.IGNORECASE)
            print(f"     [{mark}] Path {p_id}: {clean_title}")
        print()

@record_execution(stage="sense")
def main():
    frontier_path = os.path.join(repo_root, "artifacts", "frontier_state.md")
    
    import subprocess
    res = subprocess.run(["gh", "issue", "list", "--search", 'is:issue is:open label:"status: in-progress"'], capture_output=True, text=True)
    in_progress_output = res.stdout.strip()
    
    has_active_nodes = bool(in_progress_output and "no issues match" not in in_progress_output.lower())

    try:
        branch = get_current_branch(cwd=repo_root)
    except Exception:
        branch = "Unknown"
        
    open_prs = get_local_worktrees(repo_root)
    pr_count = len(open_prs)
        
    backlog_size = get_prompt_backlog_size(repo_root)

    print("=== Antigravity System Status ===")
    if has_active_nodes:
        print("Active Nodes (In-Progress):")
        print(in_progress_output)
    else:
        print("Active Nodes: None")
        
    print(f"WIP Branch  : {branch}")
    print(f"Local Worktrees: {pr_count}")
    if pr_count > 0:
        for pr in open_prs:
            print(f"  - #{pr.get('number', '?')}: {pr.get('title', 'Unknown')} ({pr.get('url', '')})")
    print(f"Prompt Queue: {backlog_size} item(s)")
    
    try:
        print_goal_progress_report()
    except Exception:
        pass

    if not has_active_nodes:
        try:
            from kernel.daemon_nba import NBADaemon
            nba = NBADaemon(repository="pltrinh1122/dyad-wu-wei")
            result = nba.evaluate(frontier_file=frontier_path, local_mode=True)
            if not result.get("recommendations"):
                result = nba.evaluate(frontier_file=frontier_path, local_mode=False)
            
            if result.get("type") in ["path_continuation", "path_switching"] and result.get("recommendations"):
                best_nba = result["recommendations"][0]
                nba_id = best_nba.get("id") or best_nba.get("number")
                print(f"\n[🤖 AUTONOMY] WIP=0 detected. Automatically acquiring lock for top NBA: Node {nba_id}...")
                import subprocess
                bin_node = os.path.join(repo_root, "bin", "node")
                process = subprocess.run([bin_node, "plan-start", str(nba_id)], capture_output=True, text=True)
                print(process.stdout)
                if process.stderr:
                    print(process.stderr, file=sys.stderr)
                
                match = re.search(r"Auto-resolved SPAO_PERSONA_ID to '([^']+)'", process.stdout)
                if match:
                    persona = match.group(1)
                    if persona != "frontier":
                        print(f"\n[🤖 DISPATCH] NBA Auto-Locked for subagent {persona}. Main Agent MUST use invoke_subagent to dispatch this node.")
        except Exception:
            pass

if __name__ == "__main__":
    main()
