# WHAT-0039: NBA Strict Transition Enforcement Gate Specification

This document defines the technical specification and interface requirements for the NBA Strict Transition Enforcement Gate.

---

## 1. Programmatic Invariants

The flow state manager and frontier editor will enforce the following invariants during lifecycle transitions:

1.  **`INVARIANT_NBA_TRANSITION_PRIORITIZED`**:
    *   Any terminal node (Activity or Probe) transitioning to an active state (i.e. status `in_progress` during `plan-start` or `checkout`) must have its parent Path ID listed in the `prioritized_paths` of an `Active` goal in the strategic intent ledger ([strategic_intent.yml](file:///mnt/shared_data/git_repos/agent-antigravity/artifacts/strategic_intent.yml)).
    *   Any path set active (via `meta path` CLI command or `set_active_path` API) must have its Path ID listed in the `prioritized_paths` of an `Active` goal.
2.  **`INVARIANT_OFFLINE_BYPASS`**:
    *   When local tests are executed (`ANTIGRAVITY_RUNNING_TESTS=1`) or offline mode is declared (`SPAO_OFFLINE=1`), live GitHub queries for parent path resolution are bypassed or mocked, allowing local execution to complete without network dependencies.

---

## 2. Interface Requirements and Hook Points

The enforcement gate must be integrated into the following modules:

### A. Parent Path Resolution
*   **Module**: `kernel/mgr_backlog.py` (or a dedicated helper in `mgr_strategic.py`).
*   **Signature**: `find_parent_path_id(node_id: str) -> str | None`
*   **Behavior**:
    1.  Query GitHub for open issues with the `path` label.
    2.  For each issue, check its body for the checkbox format matching the node: `- [ ] Node <node_id>:` or `- [x] Node <node_id>:`.
    3.  Return the path issue ID if found.

### B. Node Transition Verification Hook
*   **Module**: `kernel/mgr_strategic.py`
*   **Signature**: `verify_node_transition_allowed(node_id: str) -> None`
*   **Behavior**:
    1.  Check for `INVARIANT_OFFLINE_BYPASS`. If true, return.
    2.  Locate the parent Path ID of the node. If no parent path is found, raise `ValueError` or `Exception`.
    3.  Load active prioritized paths from `artifacts/strategic_intent.yml`.
    4.  Assert that the parent Path ID is present in the list of prioritized paths. If not, raise `Exception` to block the transition.

### C. Hook Integration Points
1.  **Node Planning Lock**: In `BaseNode.plan_start` ([node_lifecycle.py](file:///mnt/shared_data/git_repos/agent-antigravity/kernel/node_lifecycle.py)), call `verify_node_transition_allowed(self.issue_id)` inside the `FlowTransaction` context before setting status to `in_progress`.
2.  **Node Branch Checkout**: In `TerminalNode.checkout` ([node_lifecycle.py](file:///mnt/shared_data/git_repos/agent-antigravity/kernel/node_lifecycle.py)), call `verify_node_transition_allowed(self.issue_id)`.
3.  **Active Path Management**: In `set_active_path` ([mgr_frontier.py](file:///mnt/shared_data/git_repos/agent-antigravity/kernel/mgr_frontier.py)), if `path_name` is not `None` or `"None"`, extract the Path ID and verify that it exists in the strategic prioritized paths list. If not, raise an Exception.

---

## 3. Testing Requirements

*   **Offline Test Suite**: Unit tests must verify all hook point constraints using mocked/stubbed GitHub API and ledger states.
*   **Offline Isolation**: Tests must run successfully with `SPAO_OFFLINE=1` without attempting actual network connections.
