# Codifying the Meta-Orchestrator Intake Process

This document officially establishes the rigorous "Meta-Orchestrator" interaction pattern required for all Antigravity agentic repositories. It defines the core philosophy, the flow-state mechanism, and the boundaries between the Agent and the Operator.

## 1. The Core Philosophy
Modern agentic repositories abandon traditional SDLC in favor of an Agentic Architecture:
- **`artifacts/`**: Agent state, memory, schemas, and output definitions.
- **`skills/`**: Deterministic Python interfaces and tools.
- **`orchestrator/`**: Generative runtime and the live LLM SPAO loop.

The Agent is not a simple code-generator; it operates as a **Meta-Orchestrator** driving a logical, topological frontier node-by-node.

## 2. Session Continuity Invariants
Because Agent sessions are ephemeral, the repository must be physically self-describing.
- **`AGENT.md` (System Prompt)**: Mandated at the repository root. This ensures incoming sessions instantly understand their persona, architecture, and required loop mechanics.
- **`artifacts/frontier_state.md` (Macro-State)**: Mandated to track topological nodes, execution status, and feedforward invariants (knowledge required for the next node).
- **Episodic State (`task.md`)**: Strictly *optional*. Local checklist tracking in the episodic brain cache must not be relied upon for session continuity. Micro-state is deferred to GitHub Issues.

## 3. GitHub Issues as the Flow-State Ledger
GitHub Issues act as the primary operational anchor bridging the Human Operator and the Agent. To balance a cohesive narrative with granular auditability, we employ a **Hybrid Epic-Ledger Approach**:

### 3.1 The Epic Meta-Index (Macro-Ledger)
For every overarching project goal, a single long-lived "Epic" Issue must be created.
- **Purpose:** Acts as the cloud-hosted `frontier_state.md`. 
- **Mechanics:** Its body contains a Meta-Index (table of contents) tracking all completed and active Topological Nodes. It remains open until the master goal is achieved.

### 3.2 The Node Transactions (Micro-Ledger)
For every discrete Topological Node, a new specific GH-Issue must be created.
- **Contract of Execution**: The Node Issue defines the strict Scope and Acceptance Criteria (The "Plan") before execution begins. This applies to codebase mutations and **any work** performed outside the core loop.
- **Constraint Injector (HITL)**: The Operator injects feedback directly into the Node Issue's comment thread, preserving an isolated context for that specific work block.
- **Immutability:** Once a Node is complete, its Issue is closed, turning it into an immutable transaction log.

### 3.3 The Materialization Boundary (Side-Bar Rubrics)
To balance flow-state strictness with the need for rapid, low-friction brainstorming, Agents must adhere to the **Materialization Boundary**.

**Permitted Side-Bars (No GH-Issue Required):**
An Agent may converse off-ledger if the prompt satisfies these rubrics:
1. **Investigatory / Evaluative Intent:** The Operator asks to "evaluate," "explain," "assess," or "brainstorm" without commanding a state mutation.
2. **Trivially Simple Execution:** The task is a one-off operational command (e.g., `commit and push`) that does not alter architecture.
3. **Information Retrieval:** The Operator requests context extraction from the codebase.

**Mandatory Materialization (GH-Issue Required):**
The Agent **must halt conversation and demand a GH-Issue Plan** if the prompt meets these rubrics:
1. **Repository Mutation:** The prompt requires creating, deleting, or modifying files that affect the project's logic, architecture, or persistent state.
2. **Ambiguity in Implementation:** The request involves complex architecture where multiple approaches exist, requiring Operator alignment before execution.
3. **State Transitions:** The prompt commands the Agent to advance the topological frontier to a new Node.
*If an investigatory Side-Bar conversation results in a concrete decision that meets the Materialization rubrics, the Agent must immediately transition the agreed-upon decision into a formal GH-Issue.*

## 4. The SPAO + HITL Execution Loop
The master objective is decomposed into discrete topological **Nodes**. For each Node, the Agent executes the following loop:

1. **Sense**: Load invariants from `frontier_state.md` and the cloud-hosted Epic Meta-Index.
2. **Plan**: 
   - Create a **Node Issue** defining Scope and Acceptance Criteria.
   - Mutate the **Epic Issue** body to link to the newly active Node Issue.
3. **Act**: Execute codebase generation and artifact mutations.
4. **Observe (HITL Pause)**: Agent pauses. Operator executes the local environment, evaluates the state, and injects constraints. The Agent formally logs constraints to the Node Issue.
5. **Reflect & Advance**: 
   - Close the Node Issue.
   - Mutate the **Epic Issue** body to check off the completed node.
   - Feedforward learnings into `frontier_state.md` and advance the active topological node pointer.

## 5. Agent vs Operator Responsibility Matrix

| Phase | Agent Responsibilities | Operator Responsibilities |
| :--- | :--- | :--- |
| **Sense** | Parse `frontier_state.md`. Validate feedforward invariants. | Maintain clean environment state prior to session boot. |
| **Plan** | Define exact Scope and Acceptance Criteria. Create GH Issue. | Review GH Issue scope to prevent hallucinated objectives. |
| **Act** | Execute file creation, tool implementations, and orchestrator scripts. | Provide necessary external authentications (e.g., API Keys). |
| **Observe** | Await feedback. Transcribe constraints into GH Issue comments. | Execute generated code. Validate constraints. Provide HITL feedback. |
| **Reflect** | Synthesize learnings. Mutate `frontier_state.md`. Close GH Issue. | N/A |
