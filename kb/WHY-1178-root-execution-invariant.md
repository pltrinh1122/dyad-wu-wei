# WHY: The Root Execution Invariant

## Context
During Node 1149, an agent attempted to execute `bin/node reflect 1149` while its current working directory (Cwd) was set to `.worktrees/node/1149-map-backlog`. 

The Python orchestrator scripts (`kernel/daemon_node.py` and `drivers/git_client.py`) are designed to operate relative to the repository root. When the script attempted to check for merge conflicts by executing a git subprocess, it evaluated the working tree paths relative to the current Cwd.

Because the Cwd was already a nested worktree, the orchestrator attempted to double-nest the path resolution:
`FileNotFoundError: [Errno 2] No such file or directory: '/mnt/shared_data/git_repos/dyad-wu-wei/.worktrees/node/1149-map-backlog/.worktrees/node/1149-map-backlog'`

This triggered a Rollback Invariant, breaking the transaction loop and forcing the agent to reset the state.

## Core Assertion
The `kernel/` orchestrator and `drivers/` scripts resolve paths relative to the repository root directory by default. When an agent executes an orchestration transition command from within an active `.worktrees/node/<id>` subdirectory, it forces the orchestrator to resolve paths recursively, causing catastrophic failure.

## Required Pattern
To preserve architectural integrity and prevent path-resolution errors, agents MUST NEVER execute orchestration wrapper scripts (e.g. `bin/node`, `bin/prompt`, `bin/status`, `bin/backlog`) from within an active worktree subdirectory. 

The agent MUST return its Current Working Directory (Cwd) to the absolute repository root (e.g., `/mnt/shared_data/git_repos/dyad-wu-wei`) before executing any state-mutating lifecycle transition.
