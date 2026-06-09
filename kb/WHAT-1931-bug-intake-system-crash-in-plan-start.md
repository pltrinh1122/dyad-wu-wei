# WHAT: Fix System Crash in plan-start and sync (Path 1931)

## Context & The Problem
During the autonomous execution loop, a sequence of interconnected failures caused the system to crash and enter a locked state (Agentic Seizure). 

The root causes are:
1. **The Detached HEAD Push Bug**: `daemon_node.py` detaches HEAD to `origin/main` before calling `plan-start` during a sync. `node_lifecycle.py` runs `subprocess.check_call(["git", "push", "origin", "main"])` to push the `global_backlog.yml` lock commit. Since HEAD is detached, this command pushes the local `main` pointer instead of the detached HEAD, leaving the state lock commit stranded locally and leading to sync collisions.
2. **The Cache Persistency Bug**: `github_client.py` utilizes a single global timestamp for the entire `github_state_cache.json` file. Any API call (e.g. checking open issues) updates the global timestamp, which erroneously resets the TTL for unrelated cache entries like `issue_labels`. This results in "ghost labels" (e.g. `status: in-progress` persisting long after removal).
3. **The Undefined Exception**: When `plan-start` is re-run and detects an active lock in `frontier_state.yml`, it attempts to raise `StateDissonanceError`. However, this exception is not imported or defined in `node_lifecycle.py`, leading to a fatal `NameError`.

## The Goal
Fix the triad of bugs to restore systemic synchronization and locking stability.

## Technical Requirements
### 1. Fix `StateDissonanceError` in `node_lifecycle.py`
- Define `StateDissonanceError` in `kernel/agent_frontier.py` (if not already there) or just import it properly into `kernel/node_lifecycle.py` so the system can gracefully handle lock collisions.

### 2. Fix the Push Target in `node_lifecycle.py`
- Modify the git push command in `plan-start`:
  `subprocess.check_call(["git", "push", "origin", "HEAD:main"], cwd=...)`
- This ensures the commit on the detached HEAD is correctly pushed to the remote `main` branch.

### 3. Fix the Cache Timestamp in `github_client.py`
- Refactor `_get_cached_value` and `_set_cached_value` in `drivers/github_client.py` to store timestamps per-key rather than a single global timestamp.
- Example structure:
  ```json
  {
    "issue_labels": {
      "timestamp": 1234567890,
      "data": { ... }
    }
  }
  ```
- This ensures caches expire independently according to their respective TTLs.

