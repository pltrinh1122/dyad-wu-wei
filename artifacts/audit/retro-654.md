# Retrospective: Node 654 (Plan Probe)

## Failure Context
During the initiation of the Plan phase (`./bin/node plan-start 654`), the orchestrator raised a `State Dissonance` error, indicating that a previous node (Node 629) was still holding the active lock in `artifacts/frontier_state.md`. This occurred because the previous node's reflection branch was merged, but the local workspace lost the state reset when syncing detached commits.

## Root Cause
The active node pointer in the local frontier ledger was not successfully cleared during the previous loop cycles. When `plan-start` attempted to acquire the lock for Node 654, it was blocked by the stale pointer.

## Corrective Action
The lock was manually released by executing `drivers.frontier_editor.set_active_node` and `set_active_path` to `"None"`. Moving forward, the system should ensure that `sync` handles upstream active node pointer clearing robustly even when local ledger commits are detached.
