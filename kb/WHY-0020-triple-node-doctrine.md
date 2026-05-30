# WHY-0020: Triple-Node Path Initialization Doctrine

## Context
As the `dyad-wu-wei` metasystem matures, the structural integrity of the Meta-Graph becomes critical for long-term traceability and automated orchestration. We have evolved from a flat list model to a themed Path model, and recently discovered that inconsistent initialization of Paths (e.g., creating a Path without immediately populating its Meta-Index) leads to "orphaned" nodes and loss of topological clarity.

## Decision
We formally adopt the **Triple-Node Doctrine** for all Path initializations. Every new Path MUST be instantiated with exactly three specific Terminal Nodes before any functional codebase-mutating activities are added.

### The Trinity of Initialization
1.  **Align Probe**: 
    - **Scope**: Conversational and research-based alignment between the Agent and Operator regarding the Path's macro-objective, constraints, and success criteria.
    - **Outcome**: A Decision Record (`WHY-*`) or a refined Mission Statement in the Path Issue body.
2.  **Plan Probe**: 
    - **Scope**: Technical decomposition and dependency mapping for the Path subgraph.
    - **Outcome**: A fully populated Meta-Index (DAG) in the Path Issue body, ensuring all future Activities are already declared and linked.
3.  **Reflect Activity**: 
    - **Scope**: A terminal anchor node that serves as the final transition for the Path. It records the macro-learnings and verifies the closure of all child nodes.
    - **Outcome**: Path Issue is formally closed, and a Path Walkthrough/Digest is generated.

## Rationale
- **Forced Alignment**: Ensures the Agent doesn't start coding before the Operator has approved the high-level intent.
- **Topological Integrity**: The Plan Probe guarantees that the Path's "frontier" is mapped out before execution, preventing random node generation.
- **Formal Closure**: The Reflect Activity prevents Paths from remaining "ghost open" after their activities are done, providing a clean audit trail for Path-level invariants.

## Alternatives Considered
- **Dual-Probe (Align + Plan)**: Rejected because it lacks a formal terminal anchor, making Path closure ambiguous and prone to metadata drift.
- **On-Demand Creation**: Rejected as it leads to fragmented audit trails and violates the "Pre-Planned Graph" principle.
