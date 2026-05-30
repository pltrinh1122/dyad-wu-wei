# Retrospective 1521: Map Backlog Paths to Strategic Intent

## Incident Summary
During execution of Node 1521, a system crash occurred when the `reflect` command was executed from within the active `.worktrees/node/1521-map-backlog-paths` directory rather than the repository root. This caused a FileNotFoundError as the script attempted to resolve the worktree directory relative to the current directory, resulting in an invalid path `.../.worktrees/node/1521-map-backlog-paths/.worktrees/node/1521-map-backlog-paths`. Additionally, a previous attempt failed due to invalid JSON syntax in the `invariants` argument.

## Root Cause
1. The orchestrator agent ran `spao node reflect` (via `./bin/node reflect`) from within the worktree directory rather than the repository root. The node daemon expects to be run from the root directory to properly derive the worktree path.
2. The orchestrator agent passed `"['[x] mapped paths']"` instead of `'["[x] mapped paths"]'` to the `invariants` argument, causing a `JSONDecodeError`.

## Remediation
1. The orchestrator agent re-ran the `spao node reflect` command from the root directory of the repository (`/mnt/shared_data/dzw/dyad-wu-wei`).
2. The `invariants` argument was corrected to use valid JSON double quotes `["[x] mapped paths"]`.

## Structural Invariants Reinforced
- **CLI Abstraction Rule**: The `spao node reflect` command must always be executed from the root of the repository, not from within the worktree branch, as the `daemon_node.py` path resolution mechanism requires the root context.
- **JSON Arguments**: When passing JSON string arguments in the terminal, the outer quotes must be single quotes `''` and inner quotes must be double quotes `""`.
