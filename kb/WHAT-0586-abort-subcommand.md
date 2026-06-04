# WHAT-0586: Node Abort Subcommand

## Concept
A mechanism to gracefully abort an actively running SPAO node.

## Rationale
During the agent loop, if a node must be abandoned or fails due to irrecoverable context issues, the `in-progress` label and `frontier_state.md` locks remain held, preventing other agents (or the same agent later) from acquiring the node. This was observed during a collision between SG5 and SG1 on Node 525. An atomic abort mechanism is necessary to return the state to a clean `open` baseline.

## Implementation Guardrails
1. The abort action must revert the issue status to `open` (removing `in-progress`).
2. The abort action must purge the active node block from `frontier_state.yml` (and derived `.md`).
3. The abort action must forcefully clean up any associated worktree (`<id>-plan`, `<id>-act`, `<id>-observe`) to prevent local cruft.
4. The abort action must be accessible via `bin/node abort <issue_id>`.
