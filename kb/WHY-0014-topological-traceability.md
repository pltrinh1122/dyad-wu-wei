# WHY-0014: Topological Traceability Invariants

## Context
As the agentic repository grows in complexity, the queue of Backlog items (Activities and Probes) has become fragmented. Nodes are occasionally added organically without a clear overarching objective, resulting in "orphaned" tasks. Furthermore, Paths are sometimes created with a vague goal, leading to a haphazard collection of child Activities that are organically discovered during the execution process rather than deliberately designed. This organic discovery introduces execution risk, cognitive drift, and scope creep.

To harden the autonomy and mathematical traceability of the system, we must enforce strict constraints on how Nodes are bound to Paths and how Paths are initialized.

## The Orphaned Node Fallacy
An **orphaned node** is defined as an `Activity` or `Probe` in the backlog that lacks an explicit, dependency-linked parent `Path`. 

### Rationale for Elimination
1. **Loss of Traceability**: When an isolated Activity is executed, its physical mutation of the codebase cannot be traced back to a macro-level business or architectural objective. It breaks the Meta-Graph's connectivity.
2. **Context Collapse**: Agents lack the broader context of *why* the Activity is necessary. This forces the Agent to make assumptions during the implementation phase, leading to unaligned mutations.
3. **The Invariant**: **Every Terminal Node (Activity/Probe) MUST belong to a Non-Terminal parent `Path`.** If a task is too trivial to warrant a Path, it should be resolved via a lightweight `hotfix` or bundled into a broader architectural Path.

## The Dual-Probe Initialization Rule
A **Path** represents a macro-objective. Initializing a Path directly with functional `Activity` nodes forces premature execution, risking architectural misalignment before the problem is fully understood.

### Rationale for Dual-Probes
To eliminate assumptions, every `Path` MUST begin with a rigorous, purely investigatory initialization sequence composed of at least two Probes. This enforces a "think before you act" governance model at the architectural layer.

1. **Probe A: Intent & Problem Refinement**
   - **Purpose**: To interrogate the Path's objective. Before any technical scoping occurs, this Probe refines the goal, clarifies the core problem statement, and ensures the Path aligns with the repository's broader ontology.
   - **Output**: Formal `WHY-*` decision records or policy documentation.

2. **Probe B: Activity Scoping**
   - **Purpose**: To explicitly map out the necessary execution steps. Only after the problem is refined can the system determine the sequence of `Activity` nodes required to solve it. 
   - **Output**: The generation of new `Activity` issues pushed into the backlog, properly linked to the parent Path.

By enforcing the **Dual-Probe Initialization Rule**, the Meta-Graph guarantees that every functional codebase mutation (Activity) is mathematically justified by a prior phase of deliberate, documented scoping.
