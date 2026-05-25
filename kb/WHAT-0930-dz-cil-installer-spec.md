# WHAT-0930: DZ-CIL Workspace Deployment and Bootstrap Installer Specification

## Classification
- **Type**: WHAT (Technical Specification)
- **ID**: WHAT-0930
- **Author**: agent-frontier
- **Created**: 2026-05-24 (Node 930, Path 928)
- **Related Path**: Path 928 (Implement DZ-CIL Deployment and Bootstrap Installer)
- **Implements decisions from**: WHY-0929

---

### 1. Assumptions & Prerequisites
Before executing the bootstrap installer, the following conditions must be met:
1. **Core Retrieval**: The core `dz-cil` engine source code must be retrieved into a local directory (`DZ-CIL_ROOT`) by performing a `git-fetch` or `git-clone` operation.
2. **System Dependencies**: The local environment must have `python3`, `git`, and the standard `venv` module available.
3. **Execution CWD**: The initialization is invoked from the parent `DZ-CIL_ROOT` directory.

---

### 2. Unified Workspace Bootstrap Installer

We use a unified, idempotent Python bootstrapper (`bin/workspace init`) to setup a Model 1 child project workspace, replacing the legacy two-step Bash script to prevent git-clone sequencing bugs.

#### 2.1 Command Arguments
- `./bin/workspace init <repo_url>`: Initializes the remote repository inside the `./.workspace/` directory relative to the parent root.

#### 2.2 Setup Operations
The python daemon (`kernel/daemon_workspace.py`) must execute the following operations in strict order:
1. **Target Verification & Clone**: Ensure the target directory is empty or does not exist, then `git clone` the repository. This prevents Git fatal errors from non-empty directories.
2. **Directory Creation**: Create the baseline folders inside the newly cloned workspace:
   - `[TARGET_DIR]/kb/` (empty workspace knowledge base)
   - `[TARGET_DIR]/artifacts/` (workspace-specific state tracking and logs)
3. **GEMINI Invariant Injection**: Create `[TARGET_DIR]/GEMINI.md` populated with the workspace rules, explicitly indicating that the parent engine at `DZ-CIL_ROOT` is read-only.
4. **Virtual Environment Provisioning**: Initialize a local python virtual environment inside `[TARGET_DIR]/.venv/` and install `pytest`, `pytest-mock`, and `pyyaml`.
5. **Ignorance Configuration**: Append `.workspace/` to the parent `.gitignore` file and sync it to the child.

---

### 3. Workspace Worktree Redirection Spec (Model 1)

To support complex branching strategies (e.g., concurrent release branches like `v1.x` and `v1.1.x`) inside the child project workspace, we establish the **Workspace Worktree Redirection** model.

#### 3.1 Directory Layout
When the active workspace is checked out for node execution, the checkout command must NOT perform in-place checkouts. Instead, it must checkout the node branch into a git worktree located at:
```
[TARGET_DIR]/.worktrees/node/[id]-[kebab-case]/
```

#### 3.2 Redirection Logic
The node lifecycle manager (`kernel/node_lifecycle.py`) will redirect active paths when `SPAO_WORKSPACE_DIR` is set:
- **Plan Phase**: Write the Node Contract to `[TARGET_DIR]/.worktrees/node/[id]-[kebab-case]/`.
- **Act Phase**: Execute codebase modifications and run tests inside `[TARGET_DIR]/.worktrees/node/[id]-[kebab-case]/`.
- **Reflect Phase**: Clean up the worktree at `[TARGET_DIR]/.worktrees/node/[id]-[kebab-case]/` once the node is reflected and merged.
