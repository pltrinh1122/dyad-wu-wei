# WHAT-0002: Glossary of Terms

> [!NOTE]
> This glossary is the authoritative lexicon (The "What") for all domain-specific terms used across the `agent-antigravity` ecosystem. It prevents terminology drift across different models, sessions, and human operators.

---

## 🏛️ Core Ontology & Architecture

### Node
An **atomic, topological unit of work** in the repository. Every Node represents a single state transition in the repository's evolution.
* **1:1:1 Mapping**: A Node maps exactly to a **GitHub Issue** (contract/plan), a **Git Branch** (active execution), and a **Pull Request** (review/merge).
* **Isolation**: No two Nodes may be worked on concurrently (enforced by the `WIP=1` invariant).

### Probe
A **time-boxed, purely investigatory Node** designed to evaluate feasibility, research techniques, or resolve architectural ambiguity.
* **Outcome**: A Probe does **not** produce functional logic mutations. It exclusively materializes a new Decision Record (`WHY-*` document) in `kb/` or an implementation plan, feeding forward critical constraints to subsequent Nodes.

### Path
A **themed sequence of Nodes** grouped together to achieve a macro-objective.
* **Tracking**: Represented by a long-lived **Path Issue** (formerly "Epic Issue", e.g., #10) whose body contains a Meta-Index tracking the completion status of all individual topological Nodes along that path.

### Meta-Tracker
The **physical cloud container** (the specific long-lived GitHub Issue, e.g. Issue #10) representing a themed **Path**. It acts as the cloud anchor for macro-level progress tracking.

### Meta-Index
The **checklist data structure** (`- [x] Node ...`) contained inside the body of the **Meta-Tracker**. Entries index references to closed transaction issues.

---

## 🔄 Execution Loop & Governance

### SPAO Loop
The **Sense-Plan-Act-Observe** execution loop followed strictly by the Agent for every Node:
1. **Sense**: Sync `main`, clean local branches, surface pending backlog items, and validate pre-condition invariants.
2. **Plan**: Formulate the contract by creating/updating the GH Issue and linking it in the Path.
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

## 🎚️ Hierarchical Tiering & Recursive "Meta-" Prefix

To prevent conceptual confusion, we establish a strict boundary between two organizational tiers:
1. **Application Tier (The Product)**: Represents the business domain deliverables (features, bugs, stories, databases, APIs) of the client system.
2. **Metasystem Tier (The Agentic Governance System - Antigravity)**: Represents the topological, state, and cognitive engine that coordinates repository progress.

### The Taxonomy of Base Primitives
**Node**, **Path**, and **Probe** are native **Metasystem-tier primitives**. Because they *exclusively* exist within our agentic governance layer (there is no such thing as an "Application-tier Path" or "Application-tier Probe" in our codebase), prepending "Meta-" to them is redundant. We keep these base terms simple and clean.

### The Recursive "Meta-" Prefix Rule
We reserve the **"Meta-"** prefix strictly for **recursive structures** within the Metasystem tier: when a component governs, contains, or indexes other components of the *same type*:

* **Meta-Graph**: The entire Directed Acyclic Graph (DAG) of the repository's topological Nodes (vertices) linked by dependency edges. It maps the spatial evolution of the system.
* **Meta-Tracker**: A cloud container (GitHub Issue, e.g. Issue #10) that tracks *other trackers* (the individual Node issues along a Path subgraph).
* **Meta-Index**: A catalog (checklist) whose entries *index other indexes* (references to closed transaction issues).
* **Meta-Loop (SPAO Loop)**: A cyclic temporal protocol (**Sense-Plan-Act-Observe-Reflect**) governing the internal execution sequence of a single active Node.
* **Meta-Repository**: The system repository (`agent-antigravity`) hosting the rules, tools, and engine managing other codebases.
* **Meta-Orchestrator**: The generative agent engine persona (Antigravity) operating as the executive pilot.

---

## 🔁 Flow vs. Loop vs. Path (Ontological Disambiguation)

To prevent terminology drift and ensure absolute precision across models and operators, "Flow", "Loop", and "Path" represent distinct operational dimensions and must never be used interchangeably:

| Dimension | Concept | Scope | Governance |
| :--- | :--- | :--- | :--- |
| **Structural** | **Path** | A themed, directed subgraph or track within the **Meta-Graph** grouped to achieve a macro-objective (e.g. Issue #10). | Track-level roadmap progression. |
| **Spatial** | **Flow (Single-Piece Flow)** | The dynamic serialization of work *along* or *across* Paths. Enforced by the $WIP=1$ constraint, it ensures only a single vertex of the **Meta-Graph** may be active/traversed at any given moment. | Strictly enforced by the $WIP=1$ constraint. |
| **Temporal** | **Loop (Meta-Loop / SPAO)** | The cyclic 5-stage temporal execution protocol (**Sense → Plan → Act → Observe → Reflect**) executed *within* the boundaries of a single active Node (transitioning the system from one vertex to the next). | Stage-by-stage execution hygiene. |

* **Linguistic Rule**: You *run* the **Meta-Loop (SPAO Loop)** to complete a Node; this progresses the **Single-Piece Flow** sequentially along a planned **Path** within the **Meta-Graph**.

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
