# WHAT-2412: Elevate Parent Path Status Automatically

## Concept
Automatically elevate the status of a parent Path node to `status: in-progress` when a child node under it is locked (i.e. transitions to `in-progress` via `plan-start` or `checkout`).

## Goal
To ensure the UI accurately reflects the execution state by propagating the `in-progress` signal up the hierarchy from the Terminal Node to its parent Path.

## Implementation Mechanics
1. **Helper Function**: Added `_elevate_parent_path_status(issue_id: str)` to `kernel/daemon_node.py` that queries the parent via `daemon_strategic.find_parent_path_id`.
2. **Hook Locations**: This helper is called inside `plan_start_node` and `checkout_node` to ensure propagation happens during any locking event.
3. **Graceful Handling**: Errors in parent querying are caught and logged to avoid blocking the critical path of node checkout or planning.
