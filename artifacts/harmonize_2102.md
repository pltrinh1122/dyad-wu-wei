# Harmonize Path 2102: Concurrent DAG Evaluation (The Scoring Alg)

## Intent
Cognitive Offloading: We need the kernel_daemon to continuously delegate work to sub-agents safely. If an `Act` node is currently locked by a sub-agent worker, the NBA algorithm (`daemon_nba.py`) must explicitly filter it out of the available node list so we don't accidentally double-dispatch the same task.

## Structural Requirements
1. The `evaluate` method in `kernel/daemon_nba.py` must parse `artifacts/frontier_state.yml` to identify all nodes currently held by `active_agents`.
2. Any node ID that is present in the `current_active_node` of any persona MUST be excluded from the `path_continuation` recommendations.
3. This creates a Mutex Matrix where the DAG structure inherently prevents race conditions, but the scoring algorithm explicitly respects active execution locks.

## Action Plan
- Modify `kernel/daemon_nba.py` `evaluate()` to aggregate a set of `locked_node_ids` from the frontier state.
- Filter `next_nodes` in the `path_continuation` tier to ensure no locked node is recommended.
- Ensure the changes are tested via `tests/test_daemon_nba.py` to confirm filtering behavior.
