# WHAT-0092: Local-First Next-Best-Action (NBA) Evaluation Specification

## Context
During node-sync, the next-best-action hook Block-evaluates repository state by querying the remote GitHub API. Under local-by-default execution, this network query introduces ~21 seconds of latency, defeating the purpose of offline synchronization.

## Specification
The next-best-action daemon (`NBADaemon`) must support a local-first mode that eliminates all network calls.

### 1. Mode Selection
- The `NBADaemon.evaluate()` method must accept a `local_mode` boolean parameter (defaulting to `False`).
- When `local_mode=True`, the daemon must not make any calls to the GitHub API client wrappers.

### 2. Offline Backlog Extraction
- Instead of querying the remote backlog via the GitHub API, the daemon must parse the local `artifacts/frontier_state.yml` file.
- The backlog is constructed by scanning the `paths` and `nodes` recorded in `frontier_state.yml` and identifying those with a status of `Backlog`.
- Prioritization against active strategic goals must continue to use the local strategic intent ledger.

### 3. Offline Active Path Scoping
- The active path and its next eligible child nodes must be determined using the local state:
  1. Read the `Current Active Path` from the local frontier state.
  2. Parse the child nodes of the active path directly from the local `frontier_state.yml` metadata.

### 4. Hook Integration
- The `HookDaemon` next-best-action hook must check the execution context and pass the `local_mode` parameter to `NBADaemon.evaluate()`.
