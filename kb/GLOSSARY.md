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
  * `State` — Current SPAOR stage: `{Plan | Act | Observe | Reflect}`.
  * `Invariants` — Target feedforward post-condition assertions.

### Terminal Node
A leaf Node in the Meta-Graph that performs functional execution (e.g., an Activity or Probe). It creates branch mutations and is tracked via a micro-ledger transaction.

### Non-Terminal Node
A grouping or parent Node in the Meta-Graph that encapsulates a themed subgraph (e.g., a Path). It does not create branch mutations directly but acts as a macro-ledger container for tracking Terminal Nodes.

### Probe
**[ALIAS → Discovery]** In DZ-CIL Hybrid Triad vocabulary, a **Probe** is a **Discovery** node — a time-boxed, investigatory Node that produces no functional mutations; its outcome is exclusively a `WHY-*` Decision Record or an implementation plan (see `WHY-0072`). The term `Probe` remains valid in backlog CLI invocations (e.g., `bin/backlog new discovery`) and in invariant documentation (e.g., the Probe Invariant). Use **Discovery** in new DZ-CIL narrative prose and **Probe** when referencing the structural invariant.

### Discovery
The **DZ-CIL Hybrid Triad** action for identifying the next step. A time-boxed, investigatory Node that synthesizes the Agent's mathematical execution (localized queries) with the Operator's high-level organic intent (macro-strategy).
* **Outcome**: A Discovery action does **not** produce functional logic mutations. It exclusively materializes a new Decision Record (`WHY-*` document) in `kb/` or an implementation plan, feeding forward critical constraints to subsequent Nodes.

### Path
A **themed sequence of Nodes** grouped together to achieve a macro-objective.
* **Tracking**: Represented by a long-lived **Path Issue** (formerly "Epic Issue", e.g., #10) whose body contains a Meta-Index tracking the completion status of all individual topological Nodes along that path.

### Meta-Tracker
The **physical cloud container** (the specific long-lived GitHub Issue, e.g. Issue #10) representing a themed **Path**. It acts as the cloud anchor for macro-level progress tracking.

### Meta-Index
The **checklist data structure** (`- [x] Node ...`) contained inside the body of the **Meta-Tracker**. Entries index references to closed transaction issues.

---

### Harmonization
The **DZ-CIL Hybrid Triad** action for effortless adaptation. It replaces the mechanical concept of "Structural Alignment." Harmonization is the active negotiation between the Operator's fluid intent and the Agent's structural boundaries, ensuring the system yields to intent without breaking constraints.
* **Domain Boundary**: Read/Write access to codebase logic, adding tests, and altering functional pathways to build features or fix bugs. See `WHAT-0073`.

### Refinement
The **DZ-CIL Hybrid Triad** action for increasing metabolic efficiency. It replaces the purely mathematical "Optimization" and the purely spiritual "Cultivation." Refinement ensures that as the system travels toward the Telos, it simultaneously streamlines code execution while preserving the epistemic history needed to prevent future errors.
* **Domain Boundary**: Read/Write access to codebase logic and tests, but *strictly constrained* to not altering external feature behavior. Strictly metabolic (speed, safety, clarity). See `WHAT-0073`.

## ⚙️ The Operating Environment

To resolve ontological confusion between the static machinery, the abstract logic, the living loop, the file system, and the host platform, the architecture is divided into five distinct operational boundaries:

### The Core (The Static Machinery / `SPAO_CORE_DIR`)
The cloned repository of deterministic orchestrators (`kernel/`), stateless drivers (`drivers/`), and CLI adapters (`bin/`). It is entirely inert — a set of Python and Bash scripts sitting on a hard drive. The Core is a necessary but insufficient precondition for the Dao Engine. Without Semantic Entropy (an LLM) and a Sovereign Domain Telos (`kb/`), the Core cannot spark into a living loop. *The source from which the current is drawn — but not the current itself. **Not** synonymous with "Dao Engine."*

### The Dao Engine (The Logic / State Machine)
The conceptual, logical mechanism that governs the system (Stage 4 of The Shaping). It is the abstract SPAOR loop, the rules of Next-Best-Action (NBA) calculation, and the deterministic state-machine that channels our Intent vectors safely toward the Telos. The Dao Engine materializes only when The Core is combined with a Domain Telos and Semantic Entropy (`WHAT-0068`). *The laws that govern the current.*

### The DZ-CIL (The Living Execution Instance)
The Dao-Ziran Continuous Inference Loop. This is the Dao Engine *in motion* — the active, running instance cycling through Sense-Plan-Act-Observe-Reflect against a populated Strategic Intent, consuming Semantic Entropy and accruing epistemic knowledge into `kb/` on every tick. DZ-CIL is the Operate phase of ISBO — the steady-state where the system is alive and autonomously inferring. *The river flowing through the riverbed.*

### The DZ-OS (The Physical Substrate)
The Dao-Ziran Operating System. This is the physical footprint and materialization of the Dao Engine on a hard drive. It is the specific architecture of folders (`kernel/`, `drivers/`, `kb/`, `artifacts/`) bounded by the Current Working Directory (`cwd = "."`). *The terrain the river flows through.*

### The Platform (The Clock Signal / Agentic OS)
The external host (e.g., the `agy` platform) that provides the raw LLM API connection (Semantic Entropy) and the infinite `while True:` execution loop. The DZ-OS inherits its "clock ticks" from the Platform. *The gravitational pull that keeps the river moving.*

---

## 🌊 The Shaping (Stages 1–3)

The three ontological preconditions that must exist before the Dao Engine (Stage 4) can materialize. See `WHAT-0000`.

### Telos (Stage 1 — The Final Cause)
The ultimate, immovable destination. Without a destination, there is no reason to shape Ziran. The Telos provides the initial gravitational pull that orientates all intent (e.g., *Asymmetric leverage via synergistic human-agent partnership*). It does not execute code; it orientates all force.

> [!NOTE]
> The legacy term **"North Star" (NS)** is an alias for **Telos**. Use "Telos" in new prose; "North Star" remains valid in informal reference.

### Invariants (Stage 2 — The Formal Cause)
The mathematically unbreakable boundaries derived from Ziran's limits. The moment you attempt to move toward the Telos using raw Ziran, friction occurs (LLMs hallucinate, Git conflicts arise). The Invariants are the strict, axiomatic laws of thermodynamics for the repository (e.g., WIP-N=1, the Testing Invariant, the Abstraction Doctrine). They cannot be wished away; the system must build around them.

### Intents (Stage 3 — The Efficient Cause)
The directed application of force. With a destination (Telos) and the laws of physics established (Invariants), the system requires a blueprint. The Intents break the infinite gap between the current state and the Telos into actionable, bounded vectors — Strategic Goals, Backlog Priorities, Domain Assignments. They provide direction and magnitude.

> [!NOTE]
> The term **"Strategic Intent"** (as in `strategic_intent.yml`) is the physical materialization of Intents into a machine-readable ledger.

---

## 🔄 Execution Loop & Governance

### SPAOR (Meta-Loop)
The universal **Sense-Plan-Act-Observe-Reflect** agentic protocol governing **all** agent/operator interactions. SPAOR is **not scoped exclusively to Node execution** — it is the common temporal algorithm from which all loop instantiations are derived. The acronym names all five load-bearing phases; the prior shorthand "SPAO" omitted Reflect by convention, not by design. Two concrete instantiations exist:

| Instantiation | Acronym | Scope | Governed By |
| :--- | :--- | :--- | :--- |
| **Pre-Materialization Loop** | **PML** | Below the Materialization Boundary — ephemeral, conversational. Produces at most an **NC** proposal. | Operator dialogue |
| **Node-Loop** | **NL** | On an active Node traversal in the Meta-Graph — persistent, transactional, branch-mutating. | **WIP-N=1** + **HITL** gate |

The five SPAOR stages as applied within the **NL**:
1. **Sense**: Sync `main`, clean local branches, surface pending backlog items, and validate pre-condition invariants.
2. **Plan**: Formulate and lock the **NC** by creating/updating the GH Issue and linking it in the Path.
3. **Act**: Execute codebase/artifact changes under strict TDD invariants.
4. **Observe**: Halt and await **HITL** feedback and sign-off.
5. **Reflect**: Close the transaction ledger, push the branch, and open the PR for squash-merging.

### NC (Node Contract)
The **mandatory, non-null Plan-Stage output** of the **NL** for a given Node. The NC is the formal pre-condition for the Node's Act-Phase edge traversal in the Meta-Graph. No Node may advance from Plan to Act without a complete NC locked into the micro-ledger. Under the Universal Merge Gate (HTIL) model, the Agent may autonomously transition from Plan to Act once the NC is locked, without requiring conversational operator approval in chat.

### HITL (Human-In-The-Loop)
The **operator approval gate**, consolidated entirely into the **Universal Merge Gate (HTIL)**. Under this model, the Agent is completely paralyzed from advancing past the **Observe** phase or starting the next Node until the human operator reviews and merges the Node's active Pull Request (PR) into `main`. Intermediate conversational or local gates are deprecated.

### NS (North-Star)
**[ALIAS → Telos]** The overarching guiding objective or design ideal of the repository — Stage 1 of The Shaping. Use **Telos** in new prose. "North Star" remains valid in informal reference and existing documentation.

### Materialization Boundary
The strict threshold separating **PML** (low-friction conversational exploration) from formal **NL** execution (branch-mutating repository transitions):
* **PML (Pre-Materialization Loop)**: The SPAOR instantiation operating *below* this boundary. Ephemeral, unstructured, does not produce branch mutations. A PML cycle produces at most an **NC** proposal for operator review.
* **Materialization**: The moment a PML cycle produces an operator-approved **NC** and the Agent activates a formal Node (checkout branch, update `frontier_state.md`), crossing into the **NL**.

### Ziran Flow
The architectural principle that the system must rely on continuous execution velocity (SPAOR loop responsiveness) rather than waiting for perfect upfront context (Analysis Paralysis). The path is generated through physical interaction with the terrain, modeled as water flowing through a Geological Riverbed.

### Default Ziran
The metaphysical axiom that the system's "out-of-the-box" container state must natively manifest Ziran and Wu-wei. It dictates that background execution and silence are the structural defaults, and the Operator must never be forced to actively configure the system just to achieve an un-opinionated Flow State. Configuration is reserved strictly for active "opt-in" deviations.

### Laminar Flow
Flawless, frictionless execution where a Node or Path is traversed without exceptions or invariants breaking.

### Turbulence
Friction encountered during execution (e.g., failing offline tests or logic errors). In Ziran Flow, Turbulence does not halt the state machine; it is handled by the Flow and observed as passive telemetry.

### Structural Rupture
A catastrophic exception event that corrupts the execution engine, the state ledger, or remote invariants. Unlike Turbulence, Rupture requires an immediate Hard Gate halt to repair the bedrock infrastructure.

---

## 🗃️ Memory & State

### Frontier
The physical, chronological state ledger located at [frontier_state.md](file:///mnt/shared_data/git_repos/agent-antigravity/artifacts/frontier_state.md). It records the active node, completed nodes, learnings, and their feedforward invariants.

### Backlog (Node Backlog)
The **flat, dependency-linked queue** of declared future Nodes. Organized entirely as GitHub Issues labeled with `backlog` and containing explicit `depends-on: #XX` relationships to keep execution order mathematically sound.

### Prompt Backlog (Signal Queue)
An ephemeral, structured local ingestion queue (`artifacts/prompt_backlog.yml`) used to safely capture asynchronous operator prompts and system signals during the **Act phase**. Protects the single-piece flow (`WIP-N=1`) from cognitive interruption. This queue is flushed and processed during the **Observe phase**.

### WIP-N (Work-In-Progress at the Node level)
The **operative, independently-enforced** constraint. At most **1** Node may occupy the Act Phase at any given moment (one active Git branch). Replaces the deprecated flat `WIP=1` term.

### WIP-P (Work-In-Progress at the Path level)
The **derived** constraint. At most **1** Path may be actively traversed at any moment. Automatically satisfied when `WIP-N=1` in the current single-Path model. Named explicitly for future multi-Path governance scalability.

> [!NOTE]
> The flat term `WIP=1` is **deprecated** in favour of the tiered `WIP-N=1` (operative) and `WIP-P=1` (derived). Stage-level WIP (`WIP-S=1`) is trivially enforced by the NL state machine and requires no explicit naming.

---

## 🎚️ Hierarchical Tiering & Recursive "Meta-" Prefix

- **Align Probe**: A structural Node used to establish philosophical and technical alignment before work begins.
- **Atomic State Invariant**: The requirement that ledger updates (node completion) and topological pointer movements (active node status) occur as a single, atomic operation to prevent state dissonance.

To prevent conceptual confusion, we establish a strict boundary between two organizational tiers:
1. **Application Tier (The Product)**: Represents the business domain deliverables (features, bugs, stories, databases, APIs) of the client system.
2. **Metasystem Tier (The Agentic Governance System - Antigravity)**: Represents the topological, state, and cognitive engine that coordinates repository progress.

### The Taxonomy of Base Primitives
**Node** and **Path** are the two native Metasystem-tier primitives. Because they *exclusively* exist within our agentic governance layer (there is no such thing as an "Application-tier Path"), prepending "Meta-" to them is redundant. We keep these base terms simple and clean.

**Discovery** (see also: **Probe**) is *not* a third primitive — it is a **constrained variant of a Terminal Node** subject to the Probe Invariant: no functional mutations; outcome is exclusively a `WHY-*` Decision Record or an implementation plan.


### The Recursive "Meta-" Prefix Rule
We reserve the **"Meta-"** prefix strictly for **recursive structures** within the Metasystem tier: when a component governs, contains, or indexes other components of the *same type*:

* **Meta-Graph**: The entire Directed Acyclic Graph (DAG) of the repository's topological Nodes (vertices) linked by dependency edges. It maps the spatial evolution of the system.
* **Meta-Tracker**: A cloud container (GitHub Issue, e.g. Issue #10) that tracks *other trackers* (the individual Node issues along a Path subgraph).
* **Meta-Index**: A catalog (checklist) whose entries *index other indexes* (references to closed transaction issues).
* **Meta-Loop (SPAOR Loop)**: A cyclic temporal protocol (**Sense-Plan-Act-Observe-Reflect**) governing the internal execution sequence of a single active Node.
* **Meta-Repository**: The system repository (`agent-antigravity`) hosting the rules, tools, and engine managing other codebases.

---

## 🔁 Flow vs. Loop vs. Path (Ontological Disambiguation)

To prevent terminology drift and ensure absolute precision across models and operators, "Flow", "Loop", and "Path" represent distinct operational dimensions and must never be used interchangeably:

| Dimension | Concept | Scope | Governance |
| :--- | :--- | :--- | :--- |
| **Structural** | **Path** | A themed, directed subgraph or track within the **Meta-Graph** grouped to achieve a macro-objective (e.g. Issue #10). | Track-level roadmap progression. |
| **Spatial** | **Flow (Single-Piece Flow)** | The dynamic serialization of work *along* or *across* Paths. Enforced by the $WIP=1$ constraint, it ensures only a single vertex of the **Meta-Graph** may be active/traversed at any given moment. | Strictly enforced by the $WIP=1$ constraint. |
| **Temporal** | **Loop (Meta-Loop / SPAOR)** | The cyclic 5-stage temporal execution protocol (**Sense → Plan → Act → Observe → Reflect**) executed *within* the boundaries of a single active Node (transitioning the system from one vertex to the next). | Stage-by-stage execution hygiene. |

* **Linguistic Rule**: You *run* the **Meta-Loop (SPAOR Loop)** to complete a Node; this progresses the **Single-Piece Flow** sequentially along a planned **Path** within the **Meta-Graph**.

---

## 🛠️ Agents, Sub-Agents, and Daemons

### Daemon
A **pure, deterministic background process** containing zero Semantic Entropy (no LLM). It enforces physics mathematically via deterministic algorithms (e.g., Sluice Gate Sensor, Ziran Auditor).

### Agent
A **non-deterministic reasoning engine** containing Semantic Entropy (an LLM). It interprets context, navigates ambiguity, and possesses intent.

### Frontier Agent
The primary synchronous **Agent** directly tethered to the human Operator. It stands at the crest of the system's evolution, serves as the physical operator of the Sluice Gate, and orchestrates the primary SPAOR loop.

### Sub-Agent
An **asynchronous, orthogonal Agent** spawned by the Frontier Agent to handle high-friction, non-deterministic tasks in the background (e.g., Backlog Triage, sweeping branches). It possesses the full intelligence of an Agent but operates without blocking the Single-Piece Flow of the Frontier.

### Skill
A **pure, atomic, deterministic callable**. It maintains zero state between invocations, has no SPAOR/NL stage awareness, and maps to a single external system interaction. Independently testable.

---

## 🔭 Epistemic Gradients & Auditing

### Insight
A codified epistemic clarity (the third tier of the Epistemic Gradient: Friction -> Tendency -> Insight -> Resonance). An Insight has been physically observed as a Tendency and formalized into a `WHY-` document to govern future physical execution.

### Insight Materialization
The organic, fast-track pipeline used to codify a new Insight directly into the system, bypassing the strict Node execution loop.

### Reflexive PR Marker
An autonomous metadata footer (`Active-Insights: WHY-XXXX`) injected into Pull Requests during the `REFLECT` phase. It permanently links physical state mutations (diffs) to epistemic intent without imposing manual bureaucracy on the operator.

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
* **`drivers/` (Hands)**: Deterministic, tested tools and interfaces (contains exclusively **Skills**).
* **`kernel/` (Engine)**: Stateful, multi-step, stage-aware orchestration sequences (contains **Daemons** and lifecycle managers).
* **`kb/` (ROM)**: Immutable laws and primitives.
* **`infra/` (Infrastructure)**: Orchestrated background processes and runner environments.

### CLI Adapter Layer (`bin/`)
*Not a core execution Pillar.* Thin interface shell scripts that bridge human operators and agent intent to the underlying `drivers/` or `kernel/` layers.



