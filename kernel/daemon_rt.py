import sys
from drivers.file_locker import lock_file
from drivers import git_client
import yaml
import os
import argparse
import subprocess
from datetime import datetime, timezone

def get_ledger_file():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(repo_dir, "artifacts", "hotfix_ledger.yml")

def load_data(ledger_file):
    data = {"hotfixes": []}
    with lock_file(ledger_file):
        if os.path.exists(ledger_file):
            with open(ledger_file, "r") as f:
                loaded = yaml.safe_load(f)
                if loaded and "hotfixes" in loaded:
                    data = loaded
    return data

def save_data(ledger_file, data):
    os.makedirs(os.path.dirname(ledger_file), exist_ok=True)
    with lock_file(ledger_file):
        with open(ledger_file, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

def execute_hotfix(file_path, commit_msg):
    valid_exts = (".md", ".yml", ".yaml", ".gitignore")
    if not any(file_path.endswith(ext) for ext in valid_exts):
        print(f"Error: Hotfixes are strictly limited to {valid_exts}. Attempted to hotfix: {file_path}")
        sys.exit(1)
        
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        sys.exit(1)

    current_branch = git_client.get_current_branch()
    if current_branch != "main":
        print(f"Error: Hotfixes MUST be executed on the 'main' branch. You are currently on '{current_branch}'.")
        print(f"Hint: Use 'git stash', 'git switch main', run the hotfix, and then 'git switch -', 'git stash pop'.")
        sys.exit(1)

    print(f"Executing Tier-2 Hotfix for {file_path}...")
    
    # 1. git add
    git_client.add([file_path])
    
    # 2. git commit
    git_client.commit(commit_msg)
    
    # 3. git rev-parse HEAD
    commit_hash = git_client.get_commit_hash("HEAD")
    
    # 4. git push origin main
    git_client.push("main")

    # 5. append to ledger
    ledger_file = get_ledger_file()
    data = load_data(ledger_file)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    new_hotfix = {
        "hash": commit_hash,
        "timestamp": timestamp,
        "file": file_path,
        "message": commit_msg
    }
    
    data["hotfixes"].append(new_hotfix)
    save_data(ledger_file, data)
    print(f"Hotfix complete! Logged to {ledger_file}")

def execute_insight(files, title, message, insights=""):
    from drivers import github_client
    
    # Validation
    for f in files:
        if not os.path.exists(f):
            print(f"Error: File {f} does not exist.")
            sys.exit(1)
            
    current_branch = git_client.get_current_branch()
    if current_branch != "main":
        print(f"Error: Insights MUST be initiated from the 'main' branch. You are currently on '{current_branch}'.")
        sys.exit(1)
        
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    branch_name = f"rt/insight-{timestamp}"
    
    print(f"Executing Fast-Track Insight Materialization Pipeline for {len(files)} file(s)...")
    
    git_client.checkout_b(branch_name)
    git_client.add(files)
    git_client.commit(title)
    git_client.push(branch_name)
    
    if insights:
        message += f"\n\nActive-Insights: {insights}"
        
    pr_url = github_client.create_pull_request(title, message, branch_name)
    print(f"Insight PR created successfully: {pr_url}")
    
    git_client.switch("main")
    print("Switched back to main.")

def execute_score_paths(start=None, end=None):
    from kernel.nba_scorer import GranularNBAScorer
    from drivers import github_client
    
    # 1. Gather paths to evaluate
    paths_to_evaluate = []
    if start and end:
        try:
            start_val = int(start)
            end_val = int(end)
        except ValueError:
            print("Error: --start and --end must be valid integer IDs.")
            sys.exit(1)
        if start_val > end_val:
            print("Error: --start ID must be less than or equal to --end ID.")
            sys.exit(1)
            
        for issue_id in range(start_val, end_val + 1):
            try:
                labels = github_client.get_issue_labels(str(issue_id))
                if "path" in labels:
                    details = github_client.get_issue_details(str(issue_id))
                    paths_to_evaluate.append({
                        "number": str(issue_id),
                        "title": details.get("title", f"Path {issue_id}")
                    })
            except Exception:
                continue
    else:
        # Default: list all open paths
        try:
            paths_to_evaluate = github_client.list_issues_by_label("path")
        except Exception as e:
            print(f"Error listing open paths: {e}")
            sys.exit(1)
            
    if not paths_to_evaluate:
        print("No paths found to score in the specified criteria.")
        return
        
    scorer = GranularNBAScorer()
    total_score = 0.0
    
    # Generate report
    report_lines = []
    report_lines.append("# NBA Historical Decision Scoring Report")
    report_lines.append("")
    report_lines.append("This report presents Next-Best-Action (NBA) scores for the evaluated range of paths.")
    report_lines.append("Scoring methodology and rubrics are defined in [WHAT-0048-nba-scoring-rubric.md](file:///mnt/shared_data/git_repos/agent-antigravity/kb/WHAT-0048-nba-scoring-rubric.md).")
    report_lines.append("")
    report_lines.append("| Path ID | Title | Overall Score | Dependency ($C_{\\text{Dependency}}$) | Axiom ($C_{\\text{Axiom}}$) | Strategic ($C_{\\text{Strategic}}$) | Risk ($C_{\\text{Risk}}$) |")
    report_lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    
    for path in paths_to_evaluate:
        pid = path["number"]
        title = path["title"]
        try:
            res = scorer.calculate_score(pid)
            score = res.get("score", 0.0)
            comps = res.get("components", {})
            total_score += score
            report_lines.append(f"| #{pid} | {title} | {score:.3f} | {comps.get('dependency', 0.0)} | {comps.get('axiom', 0.0)} | {comps.get('strategic', 0.0)} | {comps.get('risk', 0.0)} |")
        except Exception as e:
            report_lines.append(f"| #{pid} | {title} | Error: {e} | - | - | - | - |")
            
    report_lines.append("")
    report_lines.append(f"### Total Sum of NBA Scores: {total_score:.3f}")
    
    report_content = "\n".join(report_lines)
    print(report_content)
    
    # Save the report as an artifact
    artifact_dir = "/home/pt/.gemini/antigravity-cli/brain/26a5d234-9e33-4b59-8f27-719b4738d389"
    os.makedirs(artifact_dir, exist_ok=True)
    report_file = os.path.join(artifact_dir, "nba_historical_scores_report.md")
    with open(report_file, "w") as f:
        f.write(report_content)
    print(f"\nReport saved to: {report_file}")

from kernel.daemon_telemetry import record_execution

@record_execution(stage="act")
def main():
    parser = argparse.ArgumentParser(description="Runtime Daemon (RT)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Hotfix command
    parser_hotfix = subparsers.add_parser("hotfix", help="Execute a Tier-2 hotfix on a configuration or documentation file")
    parser_hotfix.add_argument("file", help="File to hotfix")
    parser_hotfix.add_argument("message", help="Commit message")

    # Score paths command
    parser_score = subparsers.add_parser("score-paths", help="Score historical paths and output report")
    parser_score.add_argument("--start", help="Starting Path ID")
    parser_score.add_argument("--end", help="Ending Path ID")

    # Insight command
    parser_insight = subparsers.add_parser("insight", help="Fast-track an insight materialization to a PR organically without a node")
    parser_insight.add_argument("files", nargs="+", help="Files to include in the PR")
    parser_insight.add_argument("--title", required=True, help="PR Title")
    parser_insight.add_argument("--message", default="", help="PR Body")
    parser_insight.add_argument("--insights", default="", help="Active Insights (e.g., WHY-0075)")

    args = parser.parse_args()

    if args.command == "hotfix":
        execute_hotfix(args.file, args.message)
    elif args.command == "score-paths":
        execute_score_paths(args.start, args.end)
    elif args.command == "insight":
        execute_insight(args.files, args.title, args.message, insights=args.insights)

if __name__ == "__main__":
    main()
