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
GitHub Issues act as the primary operational anchor bridging the Human Operator and the Agent:
- **Contract of Execution**: The GH-Issue defines the strict Scope and Acceptance Criteria (The "Plan") before execution begins. This applies not just to codebase mutations, but to **any work** performed outside of the core loop. It forces explicit alignment.
- **Micro-State Tracker**: GH-Issues hold the granular `[ ]` task checklists.
- **Constraint Injector (HITL)**: During the Observe phase, if the Operator provides feedback or identifies missing invariants, the Agent must formally log this as a comment in the GH-Issue.
- **Flow-State Anchor**: The 1:1 mapping between a Topological Node and a GH-Issue means that if a session drops, the next session simply checks `frontier_state.md`, finds the active Node, and reads the open GH-Issue to perfectly resume flow-state.

### 3.1 The Materialization Boundary (Side-Bar Rubrics)
To balance flow-state strictness with the need for rapid, low-friction brainstorming, Agents must adhere to the **Materialization Boundary** to determine when a GH-Issue is required.

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

1. **Sense**: Load invariants from `frontier_state.md`.
2. **Plan**: Create GitHub Issue defining Scope and Acceptance Criteria.
3. **Act**: Execute codebase generation and artifact mutations.
4. **Observe (HITL Pause)**: Agent pauses. Operator executes the local environment, evaluates the state, and injects constraints. The Agent formally logs constraints to the GH Issue.
5. **Reflect & Advance**: Close GH Issue, feedforward learnings into `frontier_state.md`, and advance the active topological node pointer.

## 5. Agent vs Operator Responsibility Matrix

| Phase | Agent Responsibilities | Operator Responsibilities |
| :--- | :--- | :--- |
| **Sense** | Parse `frontier_state.md`. Validate feedforward invariants. | Maintain clean environment state prior to session boot. |
| **Plan** | Define exact Scope and Acceptance Criteria. Create GH Issue. | Review GH Issue scope to prevent hallucinated objectives. |
| **Act** | Execute file creation, tool implementations, and orchestrator scripts. | Provide necessary external authentications (e.g., API Keys). |
| **Observe** | Await feedback. Transcribe constraints into GH Issue comments. | Execute generated code. Validate constraints. Provide HITL feedback. |
| **Reflect** | Synthesize learnings. Mutate `frontier_state.md`. Close GH Issue. | N/A |
