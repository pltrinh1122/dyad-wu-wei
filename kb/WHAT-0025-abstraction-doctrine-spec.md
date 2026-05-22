# WHAT-0025: Abstraction Doctrine Specification

## 1. Subprocess API Wrappers
To comply with the Abstraction Doctrine, all shell executions of `git` and `gh` will be encapsulated behind safe Python wrapper libraries.

### `drivers/git_client.py`
A new python module to wrap Git CLI commands under the hood:
- `def add(files: list[str]) -> None`: Runs `git add <files>`
- `def commit(message: str) -> None`: Runs `git commit -m <message>`
- `def push(branch: str, force: bool = False) -> None`: Runs `git push -u origin <branch>` (or with `-f`)
- `def worktree_add(branch: str, path: str, base: str = "main") -> None`: Runs `git worktree add -b <branch> <path> <base>`
- `def worktree_remove(path: str, force: bool = False) -> None`: Runs `git worktree remove -f <path>`
- `def get_current_branch() -> str`: Runs `git rev-parse --abbrev-ref HEAD`
- `def get_commit_hash(revision: str = "HEAD") -> str`: Runs `git rev-parse <revision>`

### `drivers/github_client.py`
The existing wrapper module will be audited to ensure:
- All commands use structured JSON output (e.g. `--json`) and parse it programmatically rather than scraping text.
- No direct shell interpolation is used; commands are passed as lists to `subprocess.run` with `capture_output=True` and `text=True`.
- **Sandbox Containment**: Direct execution of `gh` or `git` commands inside scratch scripts, temporary files, or custom subprocess calls is strictly prohibited. Any required CLI command must be added to this module as a reusable python function.

---

## 2. Consolidation Evaluation: Backlog & Path
We evaluated the overlap between backlog and path responsibilities:
- **Backlog**: Inventory and registry of all work items (both paths and terminal nodes).
- **Path**: A sequential sub-graph of dependencies (Align -> Plan -> Reflect).
- **Decision**: While backlog and path represent different structures, they are highly coupled. We will consolidate path management inside `BacklogManager` in `kernel/mgr_backlog.py`:
  - `./bin/backlog` will be the unified public CLI entrypoint for both path-level and node-level work registration.
  - Active path state mutation (e.g., setting the active path) will be exposed through `BacklogManager` public methods.
  - `./bin/meta path` will be deprecated in favor of `./bin/backlog path`.

---

## 3. Node as an Internal Primitive
The `Node` lifecycle classes represent the flow state of a single leaf work item (plan, checkout, sync, reflect).
- **Enforcement**:
  - The `Node` classes in `kernel/node_lifecycle.py` will be treated as internal primitives.
  - They should only be invoked by backlog orchestration logic and admin CLI scripts (`bin/node`).
  - Developers and agents must not invoke `git` or `gh` commands directly to move a node's state; they must call the `bin/node` interface.
