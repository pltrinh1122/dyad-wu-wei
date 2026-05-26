# WHY-0986: Workspace Isolation Boundaries

## 1. Problem Statement
During execution within child workspaces or active node worktrees, file modifications can accidentally hit the repository root or the parent engine instead of targeting the active target path. This breaks the isolation boundary between parent and child contexts, causing untracked changes, main branch dirty state, and potential telemetry or config corruption.

## 2. Investigation of PR 982 Failure
The failure in PR 982 occurred when the agent attempted to edit configuration files and state ledgers, but resolved the target files to the parent engine root directory instead of the active worktree path. This happened because:
- The path resolver fell back to parent git repository directories when resolving workspace files.
- The agent lacked a strict runtime boundary guard preventing write operations outside the designated workspace.

## 3. Enforcement Specification (Strategic Guidelines)
To prevent all future boundary violations, the system must enforce the following invariants:
- **Redirection Validation**: When `SPAO_WORKSPACE_DIR` is set, all file reading/writing tools must resolve their target files relative to the child workspace root.
- **Worktree Purity Guard**: If a node worktree is active, all file mutations must be strictly locked to the worktree path (`.worktrees/node/<id>/`).
- **Telemetry Separation**: Child workspaces must maintain distinct, isolated telemetry logs to avoid colliding with parent session metrics.
