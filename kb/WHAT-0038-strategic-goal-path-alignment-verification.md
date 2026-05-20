# WHAT-0038: Strategic Goal Path Alignment Verification Specification

This document defines the specification and verification rules for programmatically enforcing the alignment of prioritized strategic path references with the live GitHub backlog state.

---

## 1. Programmatic Invariants

The ledger validation command (`./bin/strategic verify`) will enforce two new invariants on the prioritized path references:

1.  **`INVARIANT_STRATEGIC_PATH_EXISTS`**:
    *   Every Path ID listed in `prioritized_paths` under `Active` strategic goals must correspond to a valid issue in the backlog.
2.  **`INVARIANT_STRATEGIC_PATH_OPEN`**:
    *   Every Path ID listed in `prioritized_paths` under `Active` strategic goals must currently be in the `OPEN` state on GitHub.

---

## 2. Integration and Enforcement Behavior

To prevent decay of the strategic intent ledger:
*   **Command execution**: Running `./bin/strategic verify` will perform live checks against the GitHub API wrapper (`skills/github_client.py`).
*   **Strict Exit Code**: If any path violates `INVARIANT_STRATEGIC_PATH_EXISTS` or `INVARIANT_STRATEGIC_PATH_OPEN`, the tool must print a detailed error summary and terminate with a non-zero exit status (`exit 1`).

---

## 3. Environment and Test Isolation

To respect **SG-0003** (Offline Velocity Invariant), which forbids tests from making network calls:
1.  **Unit/Integration Tests**: Unit tests under `tests/` checking the strategic CLI behaviour must stub all `github_client.get_issue_details` responses.
2.  **Bypass under Local Tests**: When tests are executed via `./bin/run-tests` (or when `SPAO_OFFLINE` env variable is set), live network checks inside the strategic command are bypassed or mocked, allowing offline execution.
3.  **CI Run**: The check runs live during GitHub Actions CI execution and explicit CLI terminal invocations.
