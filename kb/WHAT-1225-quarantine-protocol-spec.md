# WHAT-1225: Quarantine Protocol Specification

## 1. Requirement Intake Issue Template
We will create a GitHub Issue Template at `.github/ISSUE_TEMPLATE/requirement_intake.md` to capture external intakes.

### Template Fields
* **name**: Requirement Intake
* **about**: Submit requirement intakes from external dyads/entities (e.g., the Healer).
* **title**: "Intake: [Short Description]"
* **labels**: `triage`
* **body**: Standard requirement template prompting the submitter for:
  - Context & Goal
  - Proposed Mechanisms
  - Strategic Harmonization

## 2. Transition Gate Enforcement
To prevent the agent or operator from executing quarantined requirements, `TerminalNode.plan_start` will enforce a strict transition check:

### The Check
Before acquiring the status lock or proceeding with planning, the node lifecycle manager must verify that the target GitHub Issue possesses the `backlog` label:
```python
labels = self.gh_labels
if "backlog" not in labels:
    raise Exception(
        f"Quarantine Protocol Violation: Node #{self.issue_id} does not possess the 'backlog' label. "
        f"Current labels: {labels}. Quarantined intake requirements must be promoted by the Operator first."
    )
```

## 3. Verification Plan
* **Unit Tests**:
  - We will add a test `test_plan_start_quarantine_violation` in `tests/test_node_lifecycle.py` that mocks `github_client.get_issue_labels` returning `["triage"]` (and lacking `backlog`), and asserts that calling `plan_start` raises the expected exception.
  - We will verify that a normal node with the `backlog` label passes the transition gate successfully.
