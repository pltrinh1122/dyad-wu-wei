# WHAT-0035: Git Transaction Ownership by SPAO Specification

This specification codifies the API extensions, CLI arguments, and execution mechanics to support unified git transaction ownership within the SPAO loop.

---

## 1. Git Client API Extensions (`drivers/git_client.py`)

All workspace mutating/inspecting functions in `drivers/git_client.py` will be extended to accept an optional `cwd` parameter (defaulting to `None`). This allows executing git subcommands relative to a specific directory (such as a partitioned worktree) without changing the process's working directory.

### 1.1 Modified Signatures
- `add(files: list[str], cwd: str | None = None)`
- `commit(message: str, cwd: str | None = None)`
- `push(branch: str, force: bool = False, cwd: str | None = None)`

---

## 2. CLI Parser Updates (`kernel/daemon_node.py`)

The `reflect` CLI parser command in `kernel/daemon_node.py` is updated to include an optional `--stage` flag.

### 2.1 Argument Definition
```python
parser_r.add_argument(
    "--stage",
    nargs="?",
    const="all",
    default="all",
    help="Granular files to stage: 'all' (default), 'none' (skip staging), or a comma-separated list of file paths."
)
```

---

## 3. Reflect Implementation & Worktree Resolution (`kernel/node_lifecycle.py`)

The `reflect` method in `TerminalNode` is refactored to dynamically resolve the worktree directory, execute staging based on the `--stage` flag, and run all git-related commands/rollbacks relative to the resolved worktree path.

### 3.1 Worktree Resolution
- Resolve the absolute path of the target worktree:
  ```python
  worktree_dir = os.path.abspath(self.get_worktree_path(branch_name))
  ```

### 3.2 Staging Execution
Based on the value of the `stage` parameter:
- **`"none"`**: Do not stage any changes (assumes files are pre-staged).
- **`"all"`** (or `None`): Auto-stage all modified and untracked changes by invoking `git_client.add(["."], cwd=worktree_dir)`.
- **Comma-separated list**: Parse paths and pass them to `git_client.add(files, cwd=worktree_dir)`.

### 3.3 Transaction Boundary Rollbacks
The transaction rollback for git commits must also target the resolved worktree path:
```python
tx.register_rollback(subprocess.run, ["git", "reset", "--hard", "HEAD~1"], cwd=worktree_dir, check=True)
```
Similarly, `_validate_spao_purity` will accept a `worktree_path` parameter and execute its `git diff` query using that directory context.
