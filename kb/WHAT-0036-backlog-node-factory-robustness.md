# WHAT-0036: Backlog Node Factory Robustness Specification

This specification formalizes the robustness invariants, API changes, and verification mechanisms for the Backlog Node Factory.

## Invariants

1. `INVARIANT_ID_BACKLOG_IDEMPOTENCY`:
   - Creating backlog issues must be idempotent. If a request is made to create a node/path that matches the title of an existing open issue, the system must log a warning and reuse the existing issue instead of creating a duplicate.
2. `INVARIANT_ID_ORPHAN_PREVENTION`:
   - Terminal nodes (Activities/Probes) must always belong to an open parent Path.
3. `INVARIANT_ID_DEPENDENCY_ENFORCEMENT`:
   - Transitioning a node via `plan-start` must fail if any dependency issue (declared in the issue's `## Depends On` section) is still `OPEN` on GitHub.
4. `INVARIANT_ID_FRONTIER_AUTO_REGISTRATION`:
   - All newly created backlog issues must be atomically appended to the local frontier ledger (`artifacts/frontier_state.yml`) with a status of `Backlog`.

---

## Technical Architecture & API Design

### 1. Idempotency Check in `BacklogManager.add`
Before calling `github_client.create_issue`:
- Query `github_client.get_open_issues()`.
- Scan open issues to find a match where the title matches:
  `f"{node_type.capitalize()}: {title}"` OR starts with `f"{node_type.capitalize()} "` and ends with `f": {title}"`.
- If found, log: `"Warning: Reusing existing issue for {node_type} '{title}'"` and return the existing issue URL.

### 2. Parent Path Verification
In `BacklogManager.add`:
- If `is_terminal` is True:
  - If `path_id` is not provided, raise `ValueError("Terminal nodes must belong to a parent Path.")`.
  - Fetch parent issue details: `github_client.get_issue_details(path_id)`.
  - Validate that the parent issue exists, has state `OPEN`, and is labeled/classified as a `Path`. If validation fails, raise `ValueError`.

### 3. Frontier Auto-Registration
In `orchestrator/mgr_frontier.py`:
- Implement a helper:
  ```python
  def register_backlog_node(filepath: str, node_id: int, node_title: str, description: str) -> None
  ```
- This helper loads the frontier state, appends the new node with `status: Backlog`, and saves/rehashes the frontier state.
- In `BacklogManager.add`, invoke `register_backlog_node` for each successfully created path/node issue.

### 4. Dependency Constraint Enforcement
In `orchestrator/node_lifecycle.py` inside `plan_start`:
- Parse the issue body to extract dependent issue IDs under `## Depends On`.
- For each dependency ID, call `github_client.get_issue_details(dep_id)`.
- If `state` is not `CLOSED`, raise `Exception("Dependency Violation: ...")`.

---

## Verification Plan

### Automated Unit Tests
1. Test idempotency behavior: verify that a duplicate title does not invoke `create_issue`.
2. Test orphan prevention: verify that creating terminal nodes with an invalid or closed parent ID raises a `ValueError`.
3. Test frontier registration: verify that a newly created issue is appended to the frontier ledger with `status: Backlog`.
4. Test dependency checking: mock a dependency issue as open and verify `plan_start` throws a dependency violation exception.
