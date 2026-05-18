# WHAT-0002: Glossary of Terms

> [!NOTE]
> This glossary is the authoritative lexicon (The "What") for all domain-specific terms used across the `agent-antigravity` ecosystem. It prevents terminology drift across different models, sessions, and human operators.

---

## 🏛️ Core Ontology & Architecture

### Node
An **atomic, topological unit of work** in the repository. Every Node represents a single state transition in the repository's evolution.
* **1:1:1 Mapping**: A Node maps exactly to a **GitHub Issue** (NC/plan), a **Git Branch** (active execution), and a **Pull Request** (review/merge).
* **Isolation**: No two Nodes may be worked on concurrently (enforced by the `WIP-N=1` invariant).
* **Mandatory Structural Attributes**: Every Node $V$ in the Meta-Graph carries the following non-nullable attributes:
  * `ID` — GitHub Issue identifier (The topological Node ID is strictly equated to its GitHub Issue ID).
  * `Title` — Concise transition description.
  * `NC` — **Non-null** Node Contract; must be locked before Act Phase entry.
  * `State` — Current SPAO stage: `{Plan | Act | Observe | Reflect}`.
  * `Invariants` — Target feedforward post-condition assertions.

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

### SPAO (Meta-Loop)
The universal **Sense-Plan-Act-Observe-Reflect** agentic protocol governing **all** agent/operator interactions. SPAO is **not scoped exclusively to Node execution** — it is the common temporal algorithm from which all loop instantiations are derived. Two concrete instantiations exist:

| Instantiation | Acronym | Scope | Governed By |
| :--- | :--- | :--- | :--- |
| **Pre-Materialization Loop** | **PML** | Below the Materialization Boundary — ephemeral, conversational. Produces at most an **NC** proposal. | Operator dialogue |
| **Node-Loop** | **NL** | On an active Node traversal in the Meta-Graph — persistent, transactional, branch-mutating. | **WIP-N=1** + **HITL** gate |

The five SPAO stages as applied within the **NL**:
1. **Sense**: Sync `main`, clean local branches, surface pending backlog items, and validate pre-condition invariants.
2. **Plan**: Formulate and lock the **NC** by creating/updating the GH Issue and linking it in the Path.
3. **Act**: Execute codebase/artifact changes under strict TDD invariants.
4. **Observe**: Halt and await **HITL** feedback and sign-off.
5. **Reflect**: Close the transaction ledger, push the branch, and open the PR for squash-merging.

### NC (Node Contract)
The **mandatory, non-null Plan-Stage output** of the **NL** for a given Node. The NC is the formal pre-condition for the Node's Act-Phase edge traversal in the Meta-Graph. No Node may advance from Plan to Act without a complete, operator-approved NC.

### HITL (Human-In-The-Loop)
The **operator approval gate**. The Agent is completely paralyzed from advancing past the **Observe** phase or starting the next Node until the human operator reviews, approves, and merges the Node's active PR into `main`.

### Materialization Boundary
The strict threshold separating **PML** (low-friction conversational exploration) from formal **NL** execution (branch-mutating repository transitions):
* **PML (Pre-Materialization Loop)**: The SPAO instantiation operating *below* this boundary. Ephemeral, unstructured, does not produce branch mutations. A PML cycle produces at most an **NC** proposal for operator review.
* **Materialization**: The moment a PML cycle produces an operator-approved **NC** and the Agent activates a formal Node (checkout branch, update `frontier_state.md`), crossing into the **NL**.

---

## 🗃️ Memory & State

### Frontier
The physical, chronological state ledger located at [frontier_state.md](file:///mnt/shared_data/git_repos/agent-antigravity/artifacts/frontier_state.md). It records the active node, completed nodes, learnings, and their feedforward invariants.

### Backlog (Node Backlog)
The **flat, dependency-linked queue** of declared future Nodes. Organized entirely as GitHub Issues labeled with `backlog` and containing explicit `depends-on: #XX` relationships to keep execution order mathematically sound.

### Prompt Backlog (Signal Queue)
An ephemeral, unstructured local ingestion queue (`artifacts/prompt_backlog.md`) used to safely capture asynchronous operator prompts and system signals during the **Act phase**. Protects the single-piece flow (`WIP-N=1`) from cognitive interruption. This queue is flushed and processed during the **Observe phase**.

### WIP-N (Work-In-Progress at the Node level)
The **operative, independently-enforced** constraint. At most **1** Node may occupy the Act Phase at any given moment (one active Git branch). Replaces the deprecated flat `WIP=1` term.

### WIP-P (Work-In-Progress at the Path level)
The **derived** constraint. At most **1** Path may be actively traversed at any moment. Automatically satisfied when `WIP-N=1` in the current single-Path model. Named explicitly for future multi-Path governance scalability.

> [!NOTE]
> The flat term `WIP=1` is **deprecated** in favour of the tiered `WIP-N=1` (operative) and `WIP-P=1` (derived). Stage-level WIP (`WIP-S=1`) is trivially enforced by the NL state machine and requires no explicit naming.

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

## 🛠️ Managers, Workflows, and Agents

### Agent
A **non-deterministic reasoning engine** (e.g., an LLM instance). It possesses intent, interprets context, and executes actions to navigate a deterministic Workflow.

### Workflow
A **deterministic state machine** and orchestration sequence. It sequences Skills across phase transitions (e.g., the SPAO loop) and maintains the rules and active state context.

### Manager (Orchestrator)
The **systemic synthesis of Workflow + Agent**. A Manager binds an Agent to a specific Workflow to achieve a domain objective.

### Operator Agent
The primary **Agent** within a Manager responsible for actively executing the functional logic of the Workflow.

### Auditor Agent
The secondary **Agent** within a Manager responsible for independent, concurrent background verification and invariant checking.

### Skill
A **pure, atomic, deterministic callable**. It maintains zero state between invocations, has no SPAO/NL stage awareness, and maps to a single external system interaction. Independently testable.

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
* **`skills/` (Hands)**: Deterministic, tested tools and interfaces (contains exclusively **Skills**).
* **`orchestrator/` (Engine)**: Generative runtime state and execution loop (contains **Workflows**).
* **`kb/` (ROM)**: Immutable laws and primitives.
* **`infra/` (Infrastructure)**: Orchestrated daemons and runner environments.

### CLI Adapter Layer (`bin/`)
*Not a core execution Pillar.* Thin interface shell scripts that bridge human operators and agent intent to the underlying `skills/` or `orchestrator/` layers.
