# WHAT-0073: DZ-CIL Domain Orthogonality

## Purpose
The DZ-CIL Hybrid Triad (Discovery, Harmonization, Refinement) must be Mutually Exclusive and Collectively Exhaustive (MECE). This document formalizes the rigid boundaries between the three actions to prevent ontological overlap and ensure the entity's path remains focused.

## The Orthogonality Matrix

### 1. Discovery (The Epistemic Boundary)
A **Discovery** node's sole purpose is to acquire knowledge and feed forward structural constraints (e.g., through an architectural Decision Record or implementation plan). 
- **Domain**: Knowledge creation and situational awareness.
- **Mutation Scope**: Strict zero logic mutation. Read-only codebase execution. Write access *only* to `kb/`, `artifacts/`, and the backlog queue.
- **Exclusivity**: If a task mutates `src/`, `drivers/`, `kernel/`, or test logic, it is *not* Discovery.

### 2. Harmonization (The Structural Boundary)
A **Harmonization** node's sole purpose is to adapt the repository's functional structure to safely satisfy the Operator's fluid intent. 
- **Domain**: Adapting the system structure (Feature logic, UI, orchestration paths).
- **Mutation Scope**: Read/Write access to codebase logic, adding tests, and altering functional pathways.
- **Exclusivity**: If a task is building a feature or fixing a bug to satisfy the Operator's intent, it is Harmonization. It must *not* be purely epistemic (Discovery), nor purely metabolic (Refinement).

### 3. Refinement (The Metabolic Boundary)
A **Refinement** node's sole purpose is to increase execution efficiency, velocity, and semantic/technical hygiene, *without* altering external feature behavior.
- **Domain**: Increasing execution efficiency, testing velocity, and cleaning technical/semantic debt.
- **Mutation Scope**: Read/Write access to codebase logic and tests, but *strictly constrained* to not altering feature behavior. 
- **Exclusivity**: If a task changes the external feature behavior or adds a new capability, it is *not* Refinement. Refinement is strictly metabolic (speed, safety, clarity, refactoring).

## MECE Synthesis
- Want to know what to do next? **Discovery**.
- Want to do the thing? **Harmonization**.
- Want to do the thing faster/safer? **Refinement**.
