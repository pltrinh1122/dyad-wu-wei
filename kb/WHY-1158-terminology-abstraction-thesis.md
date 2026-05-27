# WHY-1158: Dialectical Falsification of Terminology Abstraction Thesis

## Context
When mapping the project lifecycle, there was an initial attempt to fully abstract terminology by treating the operational git branch layer and the strategic issue/node layer as completely isomorphic or identical.

## The Terminology Abstraction Thesis (Falsified)
*Thesis:* Strategic tracking entities (Paths, Nodes, Discoveries, Activities) should map 1-to-1 directly to operational Git branches under the exact same names, treating them as the same layer of abstraction.

## The Falsification
The thesis is false because it violates the principle of layered abstraction:

1. **Strategic Layer (Paths/Nodes)**
   - Long-lived or structured graph of intent, goals, and outcomes.
   - Represented by GitHub Issues and the topological `frontier_state.md`.
   - Independent of version control mechanics.

2. **Operational Layer (Git Branches/Worktrees)**
   - Ephemeral, transient developer checkouts created for TDD cycles.
   - Constrained by Git's branch names and worktree directory structures.
   - Subject to rebase, conflict, and rollback.

## Bedrock Principle
By separating the Strategic Layer (the "What" and "Why") from the Operational Layer (the "How" and "Act"), we allow the agent to manage complex, multi-step node transitions (such as two-step planning and soft-locks) without coupling them to Git's lower-level filesystem state.
