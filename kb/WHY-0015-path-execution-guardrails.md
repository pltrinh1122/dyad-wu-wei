# WHY-0015: Path Execution Guardrails and Dynamic Traversal

This Decision Record codifies the execution invariants required to make Path traversal predictable, reliable, and strictly compliant within the agentic orchestration loop.

## The Problem
As the agent traverses a Path's Meta-Index, treating the checklist as a flat, static set of tasks leads to three critical breakdowns:
1. **Collisions:** If two Nodes overlap in operational scope, parallel execution creates race conditions, while sequential execution duplicates effort or overwrites state.
2. **Lack of Contracts:** Without mathematical input/output bounds, the Orchestrator cannot programmatically verify if a Node is allowed to start or if it has successfully completed.
3. **Traversal Ignorance:** If Node B fundamentally requires the output of Node A, a static list cannot prevent the agent from attempting Node B first.

## The Decision
To enable predictable and reliable execution of a Path, we establish the following three systemic guardrails:

### 1. The Orthogonal Scope Invariant
**All Probes and Activities must have mutually exclusive, orthogonal operational scopes.**
A Node must solve exactly one atomic sub-problem. If two items in the backlog have overlapping logic, they must be merged or rescoped before execution. This orthogonality is the foundation that prevents race conditions and strictly preserves the `WIP-N=1` and `WIP-P=1` invariants.

### 2. Pre-Requisite and Post-Requisite Contracts
**Every Node (Probe, Activity, or Path) must define strict input and output invariants.**
Nodes are not merely tasks; they are pure functions applied to the repository state. 
- **Pre-Requisite Invariants**: The precise state the repository must be in before the Node can be executed. This serves as the barrier to entry during checkout.
- **Post-Requisite Invariants**: The precise state the repository will be in after the Node successfully completes. This serves as the validation gate during reflection.

These invariants act as binding contracts that are dynamically negotiated during node linking. They allow the Path to "give weight" to completed nodes, using their Post-Requisites to satisfy the Pre-Requisites of subsequent nodes.

### 3. Dynamic Children Traversal Order
**A Path is a Directed Acyclic Graph (DAG), not a flat list. It must enforce traversal order based on context.**
Because nodes have strict Pre-Requisite contracts, the Path must honor dependencies. A Path cannot blindly iterate from top to bottom; it must dynamically evaluate which children are legally allowed to execute based on the current context.

**Crucially, this traversal order is mutable.** As additional context becomes available during execution, the Path's DAG can and should be updated. This means a new Probe or Activity can be inserted into the Path at any time, provided they meet the overall Goal/Intent of the parent Path.

## Consequences
- **Positive:** Path execution is mathematically sound. The orchestrator can natively block invalid transitions and safely execute complex, multi-step workflows.
- **Positive:** "Dog-fooding" dynamic traversal enables the system to continuously repair and adapt its own plans mid-execution by injecting new Probes as needed.
- **Negative:** Scoping out Nodes during the Plan phase is more rigorous, requiring careful definition of exact contractual bounds rather than loose human-readable tasks.
