# WHY-0037: Strategic Intent Tracking and Prioritization Enforcement

## Context

When multiple Probes and Paths coexist in the backlog, the operator can lose clarity on their relative priority and urgency because the system does not factor in the broader strategic goals. To resolve this socio-technical friction and reduce cognitive overhead, we need a formalized ledger to track the operator's strategic intent/goals and enforce sequencing of backlog items in alignment with those goals.

This document details the alignment decisions on these issues.

---

## Alignment Decisions

### 1. The Core Governance Axioms
Every strategic intent/goal must satisfy three core axioms to be considered well-formed:

- **Meta-Axiom (Falsifiability)**: All operational and strategic axioms must be testable and falsifiable. We must define a concrete signal or observation that would prove the goal is invalid or failed. If no such signal can be defined, the goal is dogmatic and must be rejected.
- **Axiom (1) (Grounding)**: Goals must be grounded in real-world human/operator problems. They cannot exist solely for codebase modularity or clean-code aesthetics. They must map to documented human friction or system failure modes experienced by the operator.
- **Axiom (2) (Constraint Separation)**: Constraints (e.g., API limits, unauthenticated runner environments) are environmental facts/boundary conditions and therefore are not the problem itself. The problem is how the system behaves under those constraints. Strategic goals must optimize system adaptability *within* constraints, not attempt to eliminate the constraint.

### 2. The Strategic Intent Ledger (`artifacts/strategic_intent.yml`)
We will establish a structured, machine-readable ledger representing the source of truth for all strategic goals.

- **Schema**:
  - `strategic_goals`: A list of goals.
    - `id`: Unique string prefix (e.g., `SG-0001`).
    - `title`: Short descriptive name.
    - `operator_problem`: Detailed grounding statement describing the human friction.
    - `constraints`: Environment boundaries/facts.
    - `falsification_signal`: Testable hypothesis or observation that would refute the goal.
    - `status`: `Draft` (in development), `Active` (currently enforcing prioritization), `Achieved` (resolved), `Falsified` (proven invalid).
    - `prioritized_paths`: Ordered list of Path/Probe issue IDs corresponding to this goal.

- **Derived Log**: A Markdown representation `artifacts/strategic_intent.md` will be auto-generated and rehashed to keep human-readable and machine-readable logs in sync.

### 3. Verification & Enforcement CLI (`bin/strategic`)
We will implement a CLI tool to manage and verify the ledger:
- `bin/strategic list`: Render active and draft goals with mapped paths.
- `bin/strategic add`: Interactively draft a goal, validating grounding, constraint formatting, and falsifiability invariants.
- `bin/strategic verify`: Assert that the ledger is structurally valid, contains no ungrounded goals, and that constraints do not frame facts as problems.
- `bin/strategic prioritize <id> <path_ids...>`: Define the sequencing of Path IDs for that goal.

### 4. Next-Best-Action (NBA) Sequencing
- **Decision**: Update `orchestrator/mgr_nba.py` to intercept global backlog recommendations. Instead of listing paths in chronological order, the recommendations must be ordered dynamically:
  1. Paths that are explicitly mapped in the `prioritized_paths` of `Active` strategic goals (in their defined sequence order).
  2. All other open backlog paths (as fallback).

---

## Invariant Formalization

A future `WHAT-*` document (to be designed in the Plan phase) will formalize the following constraints:
1. `INVARIANT_STRATEGIC_GOAL_GROUNDING`: Strategic goals must document a concrete, human-facing operator problem.
2. `INVARIANT_STRATEGIC_GOAL_CONSTRAINTS`: Context constraints must be environmental facts, not the problem.
3. `INVARIANT_STRATEGIC_GOAL_FALSIFIABILITY`: Every strategic goal must define testable falsification signals.
4. `INVARIANT_STRATEGIC_PRIORITIZATION_ENFORCEMENT`: Next-Best-Action recommendations must prioritize active strategic goals' paths.
