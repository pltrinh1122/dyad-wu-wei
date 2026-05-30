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

## The CLI Adapter vs. Domain Kernel Boundary
To preserve this ontological distinction in the implementation layer:

1. **The CLI Adapter (`bin/`)**
   - Must contain **only** thin argument parsing and proxying logic.
   - Responsible strictly for formatting operator input and passing it to the domain kernel.
   - Absolutely no core business logic, state mutations, or orchestrator state management may reside here.

2. **The Domain Kernel (`kernel/`)**
   - Must contain **all** core logic and Dao Engine state management.
   - Responsible for enforcing system invariants and orchestrating the execution loop.
   - The CLI adapter serves merely as a shell interface into this boundary-protected engine.
