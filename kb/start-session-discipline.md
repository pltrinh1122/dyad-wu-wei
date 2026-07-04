# Start-Session Discipline (d-start)

The **Start-Session Discipline** replaces automated boot hooks. It establishes a fully symmetric, manually triggered, declarative start to any session, regardless of the platform (`agy` CLI, Claude Code, or browser UI).

## The Trigger Moniker

The Operator initiates the discipline by providing the intent:

`d-start: {session goal/purpose}`

## The Execution

Upon receiving this trigger, the Agent MUST:
1. **Ground the session**: Check the baseline status of the repository (e.g., active node, uncommitted WIP, branch status) by reading the relevant state artifacts (e.g. `artifacts/frontier_state.md`) and observing the physical working tree.
2. **Lock the goal**: Explicitly adopt the provided `{session goal/purpose}` as the active Node or execution intent for the current session.
3. **Acknowledge**: Formally declare the session grounded and explicitly state the locked goal back to the Operator using the standard intent acknowledgment format.
