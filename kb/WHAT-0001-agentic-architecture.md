# WHAT-0001: Agentic Architecture & Flow-State

This document defines the *Ontology* (The "What" and "Why") of the Antigravity ecosystem. It establishes the absolute state of the universe. It does **not** contain execution instructions (for execution, see the `HOW-*` artifacts).

## 1. The Core Paradigm
Modern agentic repositories abandon traditional SDLC in favor of an Agentic Architecture. This architecture is composed of five strict pillars:
- **`artifacts/`**: The **RAM** of the system. Holds mutable Agent state, memory, schemas, and output definitions (e.g., `frontier_state.md`).
- **`skills/`**: The **Hands** of the system. Deterministic, stateless Python interfaces (**Skills**).
- **`orchestrator/`**: The **Engine** of the system. Contains stateful, stage-aware **Workflows** and the live LLM SPAO loop (e.g. `mgr_node.py`).
- **`kb/`**: The **ROM** of the system. The Knowledge Base holds the immutable Laws of the System, strictly categorized into `WHAT` (Ontology), `WHY` (Decision Records), and `HOW` (Instructions) linguistic primitives.
- **`infra/`**: The **Infrastructure** of the system. Contains Infrastructure as Code (IaC) provisioning scripts for daemons (e.g., Local CI Runners). The Agent strictly provisions infrastructure here, but does not execute the daemons directly in its cognitive loop. User-Level Systemd (`systemctl --user`) is the standard for Agent-controllable daemons.

### The CLI Adapter Layer
Bridging the operator and the architecture is the **`bin/`** directory. It is NOT a core Pillar, but rather the **CLI Adapter Layer**. It contains ultra-thin shell wrappers that delegate immediately to Python **Orchestrators** (e.g., `orchestrator/mgr_node.py`). These Python `mgr_*` orchestrators inherently own their Workflows and route execution to the underlying stateless `skills/`.

The Agent operates as a **Meta-Orchestrator**, driving a logical, topological frontier node-by-node.

### 1.1 Managers, Workflows, and Agents
To achieve true autonomy, the environment must be mathematically decoupled from the actor:
- **Workflow**: A deterministic state machine (e.g., the SPAO Loop, Node Contracts, Path Tracking). It defines the rules, transitions, and constraints of the environment.
- **Agent**: A non-deterministic reasoning engine (e.g., an LLM). It navigates and executes the workflow.
- **Manager (Orchestrator)**: The systemic synthesis of `Workflow + Agent`. A Manager binds an Agent to a specific Workflow.

### 1.2 The Dual-Agent Paradigm
A production-grade Manager cannot rely on a single thread of execution to self-police. True autonomy requires independent, concurrent verification. Therefore, a Manager consists of at least two autonomous agents:
- **Operator Agent**: Actively executes the functional logic of the Workflow (e.g., writing code, checking out branches).
- **Auditor Agent**: An independent, concurrent LLM thread responsible for continuous background verification, invariant checking, and state consistency (e.g., the Audit Daemon).

## 2. Session Continuity Invariants
Because Agent sessions are ephemeral, the repository must be physically self-describing.
- **`GEMINI.md` (System Prompt Hook)**: Mandated at the repository root. This ensures the Antigravity engine automatically injects the Meta-Orchestrator persona.
- **`artifacts/frontier_state.md` (Macro-State)**: Mandated to track topological nodes, execution status, and feedforward invariants (knowledge required for the next node).
- **Episodic State (`task.md`)**: Strictly *optional*. Local checklist tracking in the episodic brain cache must not be relied upon for session continuity. Micro-state is deferred to GitHub Issues.

## 3. GitHub Issues as the Flow-State Ledger
GitHub Issues act as the primary operational anchor bridging the Human Operator and the Agent. We employ a **Hybrid Path-Ledger Approach** (see `WHY-0001`):

### 3.1 The Path Meta-Tracker (Macro-Ledger)
For every overarching project goal, a single long-lived "Path" Issue exists, acting as the **Meta-Tracker**. It acts as the cloud-hosted `frontier_state.md`. Its description body contains the **Meta-Index** (checklist) tracking the completion status of all individual topological Nodes (vertices) along that Path subgraph in the **Meta-Graph**.

### 3.2 The Node Transactions (Micro-Ledger)
For every discrete Topological Node, a new specific GH-Issue exists, serving as a transaction ledger. 
- **Contract of Execution**: It defines the strict Scope and Acceptance Criteria (The "Plan") before execution begins.
- **Constraint Injector (HITL)**: The Operator injects feedback directly into the Node Issue's comment thread.
- **Immutability:** Once complete, its Issue is closed, turning it into an immutable transaction log.

## 4. The Materialization Boundary & The Two SPAO Instantiations
To balance flow-state strictness with rapid, low-friction brainstorming, the Agent operates in two distinct SPAO instantiations separated by the **Materialization Boundary**:

**PML (Pre-Materialization Loop)** — operates *below* the boundary:
1. **Investigatory / Evaluative Intent:** The Operator asks to "evaluate," "explain," "assess," or "brainstorm" without commanding a state mutation.
2. **Trivially Simple Execution:** One-off operational commands (e.g., `commit and push`).
3. **Information Retrieval:** Extracting context from the codebase.

A PML cycle produces at most a **Node Contract (NC)** proposal for operator review. No branch is checked out, no GitHub Node Issue is required.

**NL (Node-Loop)** — operates *above* the boundary (mandatory materialization):
1. **Repository Mutation:** Creating, deleting, or modifying files that affect logic, architecture, or persistent state.
2. **Ambiguity in Implementation:** Complex architecture requiring Operator alignment before execution.
3. **State Transitions:** Advancing the topological frontier.

Activation of the NL requires: (1) a Backlog GH Issue (created via `bin/backlog new`), (2) a complete operator-approved **NC**, (3) a checked-out `node/XX-*` branch, and (4) an updated `frontier_state.md`.

**The WHY Handoff:** *If a PML cycle results in a major architectural decision, the Agent must draft a `WHY-*` document (a Decision Record) to permanently preserve the rationale before materializing the formal GH-Issue.*

## 5. Ontological Taxonomy: Spatial (Graph) and Temporal (SPAO)

To maintain high cognitive alignment and guarantee repeatable repository transitions, the Agentic Architecture strictly segregates the following terms:

### 5.1 The Spatial Dimension (The Meta-Graph)
* **Meta-Graph**: The entire Directed Acyclic Graph (DAG) of the repository's topological Nodes (vertices) linked by dependency edges. It maps the spatial territory of the system's evolution.
* **Path**: A themed, directed subgraph or linear track within the **Meta-Graph** grouped to achieve a macro-objective.
* **Meta-Tracker (Container/Vehicle)**: The long-lived GitHub Issue (e.g., Issue #10) representing a themed Path.
* **Meta-Index (Payload/Adjacency Ledger)**: The checklist data structure (`- [x] Node ...`) contained inside the Meta-Tracker, indexing the status of the Path's vertices.

### 5.2 The Temporal Dimension (SPAO — Universal Meta-Loop)
* **SPAO (Meta-Loop)**: The **universal** 5-stage agentic protocol (**Sense-Plan-Act-Observe-Reflect**) governing **all** agent/operator interactions. SPAO is not scoped to Nodes — it is the common temporal algorithm from which all loop instantiations derive.
* **PML (Pre-Materialization Loop)**: SPAO instantiated *below* the Materialization Boundary. Ephemeral, conversational, produces at most an **NC** proposal.
* **NL (Node-Loop)**: SPAO instantiated *on* an active Node traversal in the Meta-Graph. Persistent, transactional, branch-mutating. Governed by **WIP-N=1** + **HITL**.
* **NC (Node Contract)**: The mandatory, non-null Plan-Stage output of the NL. Pre-conditions every Node's Act-Phase entry.
* **Flow (Single-Piece Flow)**: The strictly serialized traversal of vertices in the **Meta-Graph**, enforced by `WIP-N=1` (operative) and `WIP-P=1` (derived).

