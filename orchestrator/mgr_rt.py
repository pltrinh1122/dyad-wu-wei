import sys
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
    if os.path.exists(ledger_file):
        with open(ledger_file, "r") as f:
            loaded = yaml.safe_load(f)
            if loaded and "hotfixes" in loaded:
                data = loaded
    return data

def save_data(ledger_file, data):
    os.makedirs(os.path.dirname(ledger_file), exist_ok=True)
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

    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, check=True)
    current_branch = result.stdout.strip()
    if current_branch != "main":
        print(f"Error: Hotfixes MUST be executed on the 'main' branch. You are currently on '{current_branch}'.")
        print(f"Hint: Use 'git stash', 'git switch main', run the hotfix, and then 'git switch -', 'git stash pop'.")
        sys.exit(1)

    print(f"Executing Tier-2 Hotfix for {file_path}...")
    
    # 1. git add
    subprocess.run(["git", "add", file_path], check=True)
    
    # 2. git commit
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    
    # 3. git rev-parse HEAD
    result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
    commit_hash = result.stdout.strip()
    
    # 4. git push origin main
    subprocess.run(["git", "push", "origin", "main"], check=True)

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

def main():
    parser = argparse.ArgumentParser(description="Runtime Manager (RT)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Hotfix command
    parser_hotfix = subparsers.add_parser("hotfix", help="Execute a Tier-2 hotfix on a configuration or documentation file")
    parser_hotfix.add_argument("file", help="File to hotfix")
    parser_hotfix.add_argument("message", help="Commit message")

    args = parser.parse_args()

    if args.command == "hotfix":
        execute_hotfix(args.file, args.message)

if __name__ == "__main__":
    main()
