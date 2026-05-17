# WHAT-0002: Glossary of Terms

> [!NOTE]
> This glossary is the authoritative lexicon (The "What") for all domain-specific terms used across the `agent-antigravity` ecosystem. It prevents terminology drift across different models, sessions, and human operators.

---

## 🏛️ Core Ontology & Architecture

### Node
An **atomic, topological unit of work** in the repository. Every Node represents a single state transition in the repository's evolution.
* **1:1:1 Mapping**: A Node maps exactly to a **GitHub Issue** (contract/plan), a **Git Branch** (active execution), and a **Pull Request** (review/merge).
* **Isolation**: No two Nodes may be worked on concurrently (enforced by the `WIP=1` invariant).

### Spike
A **time-boxed, purely investigatory Node** designed to evaluate feasibility, research techniques, or resolve architectural ambiguity.
* **Outcome**: A Spike does **not** produce production code. It exclusively materializes a new Decision Record (`WHY-*` document) in `kb/` or an implementation plan.

### Epic
A **themed Path of Nodes** grouped together to achieve a macro-objective.
* **Tracking**: Represented by a long-lived "Epic Issue" (e.g., #10) whose body contains a Meta-Index tracking the completion status of all individual topological Nodes in that epic.

---

## 🔄 Execution Loop & Governance

### SPAO Loop
The **Sense-Plan-Act-Observe** execution loop followed strictly by the Agent for every Node:
1. **Sense**: Sync `main`, clean local branches, surface pending backlog items, and validate pre-condition invariants.
2. **Plan**: Formulate the contract by creating/updating the GH Issue and linking it in the Epic.
3. **Act**: Execute the codebase/artifact changes under strict TDD invariants.
4. **Observe**: Halt and await Human-In-The-Loop (HITL) feedback and sign-off.
5. **Reflect**: Close the transaction ledger, push the branch, and open the PR for squash-merging.

### HITL (Human-In-The-Loop)
The **operator approval gate**. The Agent is completely paralyzed from advancing past the **Observe** phase or starting the next Node until the human operator reviews, approves, and merges the Node's active PR into `main`.

### Materialization Boundary
The strict threshold dividing low-friction conversational brainstorming from formal repository mutation:
* **Side-bar**: Conversational/investigatory thread that does *not* mutate state. No GH Issue or Node is required.
* **Materialization**: The moment a side-bar converts into a formal Node because it commands a file creation, structural mutation, or state transition.

---

## 🗃️ Memory & State

### Frontier
The physical, chronological state ledger located at [frontier_state.md](file:///mnt/shared_data/git_repos/agent-antigravity/artifacts/frontier_state.md). It records the active node, completed nodes, learnings, and their feedforward invariants.

### Backlog
The **flat, dependency-linked queue** of declared future Nodes. Organized entirely as GitHub Issues labeled with `backlog` and containing explicit `depends-on: #XX` relationships to keep execution order mathematically sound.

### WIP (Work In Progress)
The volume of active development at any single moment. Under our **0-nesting single-piece flow** policy, WIP is strictly limited to **1** per repository.

---

## 📜 Linguistic Primitives (kb/ Pillars)

### Primitive
An immutable system law stored in the `kb/` (ROM) directory, classified by prefix:
* **`WHAT-*` (Definition/Ontology)**: Establishes the absolute state of the universe.
* **`WHY-*` (Decision Rationale/KDR)**: Records the philosophical reasoning behind architectural decisions.
* **`HOW-*` (Instruction/Procedure)**: Contains step-by-step instructions for loop operations.

### Feedforward Invariant
A physical post-condition/assertion of a completed Node that acts as a mandatory pre-condition for the next Node.

### Pillar
A top-level directory in the agentic architecture, defining a specific systemic function:
* **`artifacts/` (RAM)**: Mutable runtime memory and outputs.
* **`skills/` (Hands)**: Deterministic, tested tools and interfaces.
* **`orchestrator/` (Engine)**: Generative runtime state and execution loop.
* **`kb/` (ROM)**: Immutable laws and primitives.
* **`infra/` (Infrastructure)**: Orchestrated daemons and runner environments.
