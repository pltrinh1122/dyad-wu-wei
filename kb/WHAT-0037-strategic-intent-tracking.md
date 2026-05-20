# WHAT-0037: Strategic Intent Tracking and Prioritization Enforcement

This document defines the schema, validation rules, CLI interface, and Next-Best-Action (NBA) integration for the Strategic Intent Tracking subsystem.

---

## 1. Ledger Schema (`artifacts/strategic_intent.yml`)

The ledger is stored at `artifacts/strategic_intent.yml`. It has the following YAML schema:

```yaml
strategic_goals:
  - id: SG-0001
    title: "System Stability"
    operator_problem: "The operator is blind to CI test execution and suffers from random test failures."
    constraints: "CI runs in an unauthenticated environment without access to real GitHub credentials."
    falsification_signal: "We implement CI mocks, but test failures increase due to mock drift."
    status: Active # Active | Draft | Achieved | Falsified
    prioritized_paths:
      - 368
```

### Derived Markdown Document (`artifacts/strategic_intent.md`)
Every modification to the YAML file must regenerate the human-readable Markdown log and update the sha256 checksum of the ledger.

---

## 2. Invariant & Axiom Validation Rules

The CLI and the validator must enforce the following invariants on any strategic goal entry:

1. **`INVARIANT_STRATEGIC_GOAL_GROUNDING` (Axiom 1)**:
   - The `operator_problem` field must be non-empty and describe a developer-centric friction, failure, or cognitive load.
2. **`INVARIANT_STRATEGIC_GOAL_CONSTRAINTS` (Axiom 2)**:
   - The `constraints` field must be present.
   - To ensure constraints are not framed as "the problem itself", the text is scanned for forbidden action-oriented verbs (case-insensitive: "fix", "solve", "remedy", "remove", "eliminate", "correct").
3. **`INVARIANT_STRATEGIC_GOAL_FALSIFIABILITY` (Meta-Axiom)**:
   - The `falsification_signal` field must be non-empty and describe a testable observation or metric that would refute the validity of the goal.
4. **`INVARIANT_STRATEGIC_PRIORITIZATION_ENFORCEMENT`**:
   - Next-Best-Action recommendations must query the active strategic goals and prioritize paths listed in `prioritized_paths` over non-prioritized ones.

---

## 3. CLI Commands (`bin/strategic` / `orchestrator/mgr_strategic.py`)

A new script `bin/strategic` (delegating to `orchestrator.mgr_strategic`) will expose:

* **`list`**: Render all strategic goals in a clean, hierarchical table format grouped by status (`Active`, `Draft`, `Achieved`, `Falsified`).
* **`add`**: Interactive prompt to draft a new strategic goal. Validates inputs against all invariants before writing. Assigns incremental ID (`SG-0001`, `SG-0002`, etc.).
* **`verify`**: Scan the ledger, running all validation rules. Output success or a detailed checklist of failures. Also warn if any open backlog Path issue is not mapped to any active strategic goal.
* **`prioritize <id> <path_ids...>`**: Sequence Path IDs under the specified goal's `prioritized_paths`.
* **`transition <id> <status> [notes]`**: Move a goal's status. If transitioning to `Falsified`, the operator must provide notes detailing the signal witnessed.

---

## 4. Next-Best-Action (NBA) Integration

In `orchestrator/mgr_nba.py`:
- Load `artifacts/strategic_intent.yml` if it exists.
- Extract the ordered list of all `prioritized_paths` from `Active` strategic goals.
- In `NBAManager.evaluate`, intercept the global backlog recommendation list:
  1. Order paths that match `prioritized_paths` first (preserving the order of priority).
  2. Append other open backlog paths below them.
