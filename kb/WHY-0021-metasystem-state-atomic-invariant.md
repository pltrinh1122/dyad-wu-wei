# WHY-0021: The Atomic State Invariant

## Context
The Antigravity Metasystem relies on a topological ledger (`frontier_state.md`) to track the agent's progress through the state-space. Historically, the process of marking a node as `Completed` (ledger update) and clearing the `Current Active Node` (pointer transition) were decoupled. This led to "stale pointers" (ghost state) where the system appeared to be stuck in a completed node.

## The Invariant
**Ledger updates and topological pointer transitions MUST be atomic.**

No transaction shall mark a Node or Path as `Completed` without simultaneously releasing its "Active" status in the same file-write operation.

## Principles
1. **Topological Integrity**: The `Current Active Node` pointer must always accurately reflect the physical reality of the workspace.
2. **Audit-First Design**: The system must be capable of detecting dissonance (e.g., a completed node still marked as active) and halting execution immediately.
3. **Self-Healing Automation**: Tools like `frontier_editor` must enforce this atomicity at the primitive level, removing the burden of manual pointer management from the higher-level orchestrators.

## Consequences of Violation
Dissonance in the state ledger leads to:
- Incorrect NBA (Next Best Action) evaluation.
- False "In Progress" locks preventing new work.
- Decay of the Agentic SPAO loop logic.
