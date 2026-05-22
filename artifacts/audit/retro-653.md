# Retrospective: Node 653 (Align Probe)

## Failure Context
During the reflection phase, a `FileNotFoundError` was raised because the `./bin/node reflect` command was executed from within the active `.worktrees/node/653-align-meta-domain` directory instead of the repository root. The script internally appended the worktree path again, causing the invalid path.

## Root Cause
The orchestrator scripts (`mgr_node.py`) expect to be run from the repository root, as they handle worktree pathing internally.

## Corrective Action
Execute all SPAO loop CLI commands (e.g., `bin/node reflect`) exclusively from the repository root (`/mnt/shared_data/git_repos/agent-antigravity`). Do not `cd` into the `.worktrees` directory to run lifecycle commands.
