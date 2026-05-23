# WHAT-0027: Abstraction Doctrine Remediation & Atomic Transaction Specification

This document provides the technical design, API specifications, and refactoring guidelines to remediate remaining raw shell subprocess executions and implement transactional rollback capability across node/backlog lifecycle states.

## 1. Skill Extensions

We will extend `drivers/git_client.py` and `drivers/github_client.py` to encapsulate the remaining raw commands.

### A. Extended `drivers/git_client.py`
Add the following functions:

```python
@record_execution(stage="skill")
def switch(branch: str) -> None:
    """Switches to the specified branch."""
    subprocess.run(["git", "switch", branch], check=True)

@record_execution(stage="skill")
def pull(remote: str, branch: str, prune: bool = False) -> None:
    """Pulls commits from remote repository branch."""
    cmd = ["git", "pull"]
    if prune:
        cmd.append("--prune")
    cmd.extend([remote, branch])
    subprocess.run(cmd, check=True)

@record_execution(stage="skill")
def list_merged_branches() -> list[str]:
    """Returns a list of local branches that have been merged into HEAD."""
    res = subprocess.run(["git", "branch", "--merged"], capture_output=True, text=True, check=True)
    return [b.strip().strip("* ") for b in res.stdout.splitlines() if b.strip()]

@record_execution(stage="skill")
def list_local_branches() -> list[str]:
    """Returns a list of all local branch names."""
    res = subprocess.run(["git", "branch", "--format", "%(refname:short)"], capture_output=True, text=True, check=True)
    return [b.strip() for b in res.stdout.splitlines() if b.strip()]

@record_execution(stage="skill")
def worktree_prune() -> None:
    """Prunes stale git worktrees."""
    subprocess.run(["git", "worktree", "prune"], check=False)

@record_execution(stage="skill")
def get_git_common_dir() -> str:
    """Returns the .git directory path (git-common-dir)."""
    res = subprocess.run(["git", "rev-parse", "--git-common-dir"], capture_output=True, text=True, check=True)
    return res.stdout.strip()

@record_execution(stage="skill")
def get_show_toplevel() -> str:
    """Returns the primary repository root directory."""
    res = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
    return res.stdout.strip()
```

---

## 2. Refactoring Targets

Refactor the following components to replace direct subprocess invocations:

### A. `kernel/node_lifecycle.py`
- **Line 175 (in `plan_finish`)**:
  ```diff
  -res = subprocess.run(["gh", "issue", "view", self.issue_id, "--json", "title"], capture_output=True, text=True, check=True)
  -current_title = json.loads(res.stdout)["title"]
  +issue_details = github_client.get_issue_details(self.issue_id)
  +current_title = issue_details.get("title", "")
  ```

### B. `kernel/daemon_node.py`
- **Line 42–43 (in `sync_and_clean_node`)**:
  ```diff
  -subprocess.run(["git", "switch", "main"], check=True)
  -subprocess.run(["git", "pull", "--prune", "origin", "main"], check=True)
  +git_client.switch("main")
  +git_client.pull("origin", "main", prune=True)
  ```
- **Line 48 (in `sync_and_clean_node`)**:
  ```diff
  -result = subprocess.run(["git", "branch", "--merged"], capture_output=True, text=True)
  -for branch in result.stdout.split('\n'): ...
  +for branch in git_client.list_merged_branches(): ...
  ```
- **Line 64 (in `sync_and_clean_node`)**:
  ```diff
  -result = subprocess.run(["git", "branch", "--format", "%(refname:short)"], capture_output=True, text=True)
  -local_branches = {b.strip() for b in result.stdout.split('\n') if b.strip()}
  +local_branches = set(git_client.list_local_branches())
  ```
- **Line 71 (in `sync_and_clean_node`)**:
  ```diff
  -subprocess.run(["git", "worktree", "prune"], check=False)
  +git_client.worktree_prune()
  ```
- **Line 122 (in `cmd_view`)**:
  ```diff
  -res = subprocess.run(['gh', 'issue', 'view', args.issue_id, '--json', 'title,state,body'], capture_output=True, text=True, check=True)
  -data = json.loads(res.stdout)
  +data = github_client.get_issue_details(args.issue_id)
  ```

### C. `kernel/daemon_telemetry.py`
- **Line 80 & 83 (in `_get_default_ledger_path`)**:
  ```diff
  -common_dir = subprocess.check_output(["git", "rev-parse", "--git-common-dir"], text=True).strip()
  +common_dir = git_client.get_git_common_dir()
  ...
  -toplevel = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
  +toplevel = git_client.get_show_toplevel()
  ```

---

## 3. Transaction Boundary (`kernel/daemon_transaction.py`)

A new transaction manager, `FlowTransaction`, will wrap all phase state transitions.

```python
import os
import shutil
import tempfile

class FlowTransaction:
    """Manages the transactional context and rollback logic for orchestration tasks."""
    
    def __init__(self, frontier_file: str = "artifacts/frontier_state.md"):
        self.frontier_file = frontier_file
        self.yml_file = frontier_file.replace(".md", ".yml")
        self.sha_file = frontier_file.replace(".md", ".yml.sha256")
        
        self.rollback_stack = []
        self.temp_dir = None
        self.backups = {}

    def __enter__(self):
        # Create temp dir for backups
        self.temp_dir = tempfile.mkdtemp()
        
        # Backup frontier state ledger files
        for path in [self.frontier_file, self.yml_file, self.sha_file]:
            if os.path.exists(path):
                backup_name = os.path.basename(path) + ".bak"
                backup_path = os.path.join(self.temp_dir, backup_name)
                shutil.copy2(path, backup_path)
                self.backups[path] = backup_path
                
        return self

    def register_rollback(self, func, *args, **kwargs):
        """Pushes a rollback action to the transaction stack."""
        self.rollback_stack.append((func, args, kwargs))

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Transaction failed! Roll back mutations
            print(f"\n⚠️ FlowTransaction failed: {exc_val}")
            print("Initiating rollback actions...")
            
            # 1. Restore frontier state backup files
            for original, backup in self.backups.items():
                if os.path.exists(backup):
                    shutil.copy2(backup, original)
            
            # 2. Run registered cleanup/rollback calls in reverse order
            for func, args, kwargs in reversed(self.rollback_stack):
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print(f"Error during rollback: {e}")
                    
        # Cleanup backup files
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
```

### Usage inside `TerminalNode` Lifecycle Methods:
```python
def plan_start(self, frontier_file: str = "artifacts/frontier_state.md") -> None:
    with FlowTransaction(frontier_file) as tx:
        self._verify_state_purity(frontier_file)
        
        in_progress_label = load_node_status_config().get("in_progress", "status: in-progress")
        if in_progress_label in self.gh_labels:
            raise Exception("already in progress")
            
        self._validate_orthogonal_scope()
        self.set_status("in_progress")
        
        # Register rollback to remove the label on failure
        tx.register_rollback(github_client.remove_label, self.issue_id, in_progress_label)
        
        details = github_client.get_issue_details(self.issue_id)
        node_title = details.get("title", f"Node {self.issue_id}")
        agent_frontier.append_active_node(frontier_file, int(self.issue_id), node_title, "Planning Phase", [])
```
Similar transactional context management will be implemented for `checkout` and `reflect` transitions.
