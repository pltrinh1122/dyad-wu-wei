# WHY-0989: Workspace Isolation Boundaries and Decoupling Invariants

## Classification
- **Type**: WHY (Decision Rationale)
- **ID**: WHY-0989
- **Author**: agent-sg5
- **Created**: 2026-05-27 (Node 989, Path 985)

---

## 1. Context
During reflection operations inside a checked-out child workspace, parent files and tracking state (`frontier_state.*`) tended to bleed or overwrite configurations in the parent repository root.

## 2. Decision
To resolve this, we mandate that:
1. All file mutations, commits, and tests must target the active workspace directory relative path.
2. The orchestrator must validate path constraints to mathematically block any copy or edit actions targeting files outside the sandbox boundary.

## 3. Implications
- Ensures parent repository state remains clean when executing in parallel, sovereign child workspaces.
