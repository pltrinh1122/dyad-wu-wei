# WHY-1154: Core and Dao Engine Ontological Distinction

## Context
A key source of confusion in autonomous systems is the conflation of the codebase itself with the active running agent loop.

## Ontological Boundary
We establish the formal ontological distinction between:

1. **The Core (Static ROM)**
   - The static codebase, configuration files, templates, and specifications defined in the repository.
   - It represents the immutable laws, memory templates, and behavioral constraints.
   - It is static on disk and does not carry runtime state.

2. **The Dao Engine (Dynamic Runtime)**
   - The active execution state, runtime daemon context, worktrees, locks, and temporal files materialized during execution.
   - It represents the flow of action, sensing, decision-making, and execution (Ziran and Wu-wei).
   - It is transient, stateful, and dynamically resolves paths and configurations at runtime.

## Bedrock Principle
The Core acts as the genetic code (ROM), whereas the Dao Engine represents the living organism executing within its environment. The Dao Engine must always respect and enforce the invariants defined in the Core, but the Core itself must remain clean of dynamic runtime leakage (e.g. root state mutations).
