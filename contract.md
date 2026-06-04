## Goal
Implement bin/node abort to atomically release an in-progress plan-start lock

## Specification
See kb/WHAT-0586-abort-subcommand.md

## Execution Plan
1. Add `abort_active_node` to `kernel/agent_frontier.py` to cleanly delete the node from the `nodes` block.
2. Add `abort()` to `TerminalNode` in `kernel/node_lifecycle.py` to revert label to `open`, purge worktree, and call `abort_active_node`.
3. Add `cmd_abort` to `kernel/daemon_node.py` and register the `abort` subparser.
4. Add tests for `abort` flow.
