# WHAT-0987: Workspace Isolation Boundaries Specification

## 1. Boundary Assertion Rules
To prevent file mutation leakage to the parent repository root, the system must enforce strict runtime path checks on all code writing and modifying tools.

## 2. Directory Validation Schema
When a tool executes a file creation or replacement operation, it must validate the target file's absolute path using the following hierarchy:

1. **Active Worktree Boundary**: If the agent is executing inside an active SPAO node session, the absolute path of the target file `F` must reside within the worktree directory `W`:
   $$\text{is\_subpath}(F, W) = \text{True}$$
2. **Sovereign Workspace Boundary**: If the environment variable `SPAO_WORKSPACE_DIR` is set, the absolute path of the target file `F` must reside within the workspace directory `S`:
   $$\text{is\_subpath}(F, S) = \text{True}$$

## 3. Violation Handling
If the target file path fails the boundary assertion checks, the tool must:
- Abort the write operation immediately before touching the filesystem.
- Raise a `ValueError` or a specialized boundary violation exception.
- Log a FAILURE event in the telemetry stream.
