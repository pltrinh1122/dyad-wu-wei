import time
import os
import yaml
import shutil
from unittest.mock import patch

# Setup sys.path to resolve kernel and drivers
import sys
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
os.environ["PYTHONPATH"] = repo_root + os.path.pathsep + os.environ.get("PYTHONPATH", "")

from kernel.daemon_node import sync_and_clean_node

def main():
    prompt_backlog_path = os.path.join(repo_root, "artifacts", "prompt_backlog.yml")
    backup_path = os.path.join(repo_root, "artifacts", "prompt_backlog.yml.bak")

    # 1. Backup prompt backlog
    if os.path.exists(prompt_backlog_path):
        shutil.copy2(prompt_backlog_path, backup_path)
    
    # Ensure starting in a clean local mode state
    with open(prompt_backlog_path, "w") as f:
        yaml.safe_dump({"prompts": []}, f)

    try:
        # 2. Benchmark Local Mode (Offline-by-Default)
        local_durations = []
        for i in range(3):
            # Clean root changes that might occur during switch/sync
            subprocess_run_checkout(repo_root)
            
            # Patch WIP-N=1 checks
            with patch("kernel.daemon_node.get_local_worktrees", return_value=[]), \
                 patch("kernel.daemon_node.github_client.get_open_prs", return_value=[]):
                start = time.time()
                sync_and_clean_node()
                duration = time.time() - start
                local_durations.append(duration)
        
        avg_local = sum(local_durations) / len(local_durations) if local_durations else 0.0

        # 3. Queue Sluice Gate Open prompt for Remote Mode
        sluice_prompt = {
            "id": "p-benchmark-temp",
            "timestamp": "2026-05-23T00:00:00Z",
            "text": "[NOTIFICATION] Sluice Gate Opened: PR for Node benchmark",
            "status": "pending"
        }

        # 4. Benchmark Remote Mode
        remote_durations = []
        for i in range(3):
            # Put prompt back since sync consumes it
            with open(prompt_backlog_path, "w") as f:
                yaml.safe_dump({"prompts": [sluice_prompt]}, f)
            subprocess_run_checkout(repo_root)
            
            with patch("kernel.daemon_node.get_local_worktrees", return_value=[]), \
                 patch("kernel.daemon_node.github_client.get_open_prs", return_value=[]):
                start = time.time()
                sync_and_clean_node()
                duration = time.time() - start
                remote_durations.append(duration)

        avg_remote = sum(remote_durations) / len(remote_durations) if remote_durations else 0.0

        # 5. Restore prompt backlog & clean workspace
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, prompt_backlog_path)
            os.remove(backup_path)
        subprocess_run_checkout(repo_root)

        # Output report
        print("# `bin/node sync` Performance Analysis Report")
        print("\n| Run | Local Mode (Offline) | Remote Mode (Online) |")
        print("| :--- | :--- | :--- |")
        for idx in range(3):
            loc_val = f"{local_durations[idx]:.3f}s" if idx < len(local_durations) else "N/A"
            rem_val = f"{remote_durations[idx]:.3f}s" if idx < len(remote_durations) else "N/A"
            print(f"| Run {idx+1} | {loc_val} | {rem_val} |")
        
        print(f"| **Average** | **{avg_local:.3f}s** | **{avg_remote:.3f}s** |")
        
        if avg_local > 0:
            speedup = avg_remote / avg_local
            print(f"\n🚀 **Speedup Factor**: {speedup:.2f}x faster in Local Mode (offline-by-default).")
        else:
            print("\nError calculating speedup.")

    except Exception as e:
        print(f"Benchmark error: {e}")
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, prompt_backlog_path)
            os.remove(backup_path)

def subprocess_run_checkout(repo_root):
    from drivers import git_client
    git_client.restore([
        "artifacts/frontier_state.md",
        "artifacts/frontier_state.yml",
        "artifacts/frontier_state.yml.sha256"
    ], cwd=repo_root)

if __name__ == "__main__":
    main()
