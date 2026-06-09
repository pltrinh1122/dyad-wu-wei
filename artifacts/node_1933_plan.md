# Node 1933: Implementation Contract for System Crash Bug Fixes

## 1. Technical Design
### `StateDissonanceError` Resolution
- Add `class StateDissonanceError(Exception): pass` to `kernel/node_lifecycle.py`.

### Detached HEAD Push Fix
- Replace `["git", "push", "origin", "main"]` with `["git", "push", "origin", "HEAD:main"]` in:
  - `kernel/node_lifecycle.py`
  - `kernel/daemon_backlog.py`
  - `kernel/daemon_node.py`

### Cache Persistency Fix
- Update `drivers/github_client.py` to store cache entries as `{"timestamp": int, "data": value}`.
- Update `_get_cached_value` and `_set_cached_value` to utilize the per-key timestamp instead of a global `timestamp`.

## 2. Testing Strategy
- Run `spao test` (or `./bin/run-tests`) locally to ensure the test suite passes with these changes.
- The `StateDissonanceError` should be importable.
- The `github_client.py` cache functions should successfully serialize and deserialize the new format.

## Depends On
None
