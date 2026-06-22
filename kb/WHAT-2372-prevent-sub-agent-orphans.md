# WHAT-2372: Prevent Sub-agent Orphans via Execution Audit and CSI Guards

## 1. Intent & Problem Statement
The intent of this specification is to maintain metasystem integrity and prevent the backlog from polluting the Semantic Dispatcher with stale state, ensuring the Factory Floor only operates on actively verified DAGs.

Currently, sub-agents (acting via the Antigravity system and invoking commands) can abandon nodes without cleaning up, leading to orphaned locks. This occurs in two primary scenarios:
1. **Systemic Crash within the Node Lifecycle (`kernel/daemon_node.py`)**: An unhandled exception occurs during `bin/node` execution. The exception is caught, a bug is logged, but the node lock (`status: in-progress`) is not released.
2. **Silent AI Sub-agent Crash**: The Antigravity LLM backend encounters an API/Token failure and terminates silently. The `bin/node` execution is never resumed, leaving the node indefinitely locked.

## 2. Technical Design: CSI Guards

### Guard A: Global Exception Handler Lock Release (`kernel/daemon_node.py`)
A CSI Guard must be injected into the global `except Exception:` block of `kernel/daemon_node.py`'s `main()` function.

- **Trigger:** Unhandled exception during any CLI execution sequence.
- **Action:** If an active issue lock can be detected (via CLI arguments or by reading `frontier_state.yml`), the guard must explicitly call `github_client.remove_label` to clear the `status: in-progress` label and push the node back to the `status: triage` queue. It will also invoke `node.abort()` to reset the local ledger.

### Guard B: Active Autonomous Abort for Silent Crashes (`drivers/audit_daemon.py`)
The existing `evaluate_liveness_stall` rule handles silent sub-agent seizures by alerting the prompt queue, but it stops short of active remediation.

- **Trigger:** `evaluate_liveness_stall` detects that `frontier_state.yml` has not been modified within the `stall_threshold_minutes` while a node is marked Active.
- **Action:** Enhance the daemon to actively execute `subprocess.run(["./bin/node", "abort"])` to forcibly release the node lock and clean up the worktree, rather than just passively alerting.

## 3. Sub-Nodes (DAG)
- **Node 2372**: Plan - Formulate the technical design and diffs for a new CSI Guard to prevent orphans.
- **Node 2373**: Act - Implement Guard A (Global Exception Release) and Guard B (Autonomous Abort).
- **Node 2374**: Reflect - Validate the implementation.
