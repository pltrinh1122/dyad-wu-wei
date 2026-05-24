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
1. **Core Retrieval**: The Operator has retrieved the core `dz-cil` engine source code from the remote repository (e.g. `pltrinh1122/agent-antigravity`) into a local directory (`DZ-CIL_ROOT`) by performing a `git-fetch` or `git-clone` operation. This directory serves as the read-only framework source.
2. **System Dependencies**: The local environment must have `python3`, `pip`, `virtualenv` (or python standard library `venv`), and `git` installed and available in the system `PATH`.
3. **Execution CWD**: The installer script `bin/dz-cil-install` is invoked from the parent `DZ-CIL_ROOT` directory.

---

### 2. Unified Workspace Bootstrap Installer

We will implement a new, idempotent shell script `bin/dz-cil-install` (or `bin/dz-cil_install.sh`) to bootstrap a Model 1 child project workspace.

#### 2.1 Command Arguments & Options
- `bin/dz-cil-install [DIR]`: Initialize a workspace inside the specified directory (defaults to `./.workspace/` relative to parent root).
- `bin/dz-cil-install --help`: Print usage instructions.

#### 2.2 Setup Operations
The installer must execute the following operations in order:
1. **Directory Creation**: Create the target workspace directory and its baseline folders:
   - `[TARGET_DIR]/kb/` (empty workspace knowledge base)
   - `[TARGET_DIR]/artifacts/` (workspace-specific state tracking and logs)
2. **Ignorance Configuration**: Append `[TARGET_DIR]/` (e.g. `.workspace/`) to the parent `.gitignore` file.
3. **GEMINI Invariant Injection**: Create `[TARGET_DIR]/GEMINI.md` populated with the workspace rules, explicitly indicating that the parent engine at `DZ-CIL_ROOT` is read-only.
4. **Virtual Environment Provisioning**: Initialize a local python virtual environment inside `[TARGET_DIR]/.venv/` and install `pytest`, `pytest-mock`, and `pyyaml`.

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
