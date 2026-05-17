# WHAT-0001: Agentic Architecture & Flow-State

This document defines the *Ontology* (The "What" and "Why") of the Antigravity ecosystem. It establishes the absolute state of the universe. It does **not** contain execution instructions (for execution, see the `HOW-*` artifacts).

## 1. The Core Paradigm
Modern agentic repositories abandon traditional SDLC in favor of an Agentic Architecture. This architecture is composed of four strict pillars:
- **`artifacts/`**: The **RAM** of the system. Holds mutable Agent state, memory, schemas, and output definitions (e.g., `frontier_state.md`).
- **`skills/`**: The **Hands** of the system. Deterministic Python interfaces and tools.
- **`orchestrator/`**: The **Engine** of the system. Generative runtime and the live LLM SPAO loop.
- **`kb/`**: The **ROM** of the system. The Knowledge Base holds the immutable Laws of the System, strictly categorized into `WHAT` (Ontology), `WHY` (Decision Records), and `HOW` (Instructions) linguistic primitives.
- **`infra/`**: The **Infrastructure** of the system. Contains Infrastructure as Code (IaC) provisioning scripts for daemons (e.g., Local CI Runners). The Agent strictly provisions infrastructure here, but does not execute the daemons directly in its cognitive loop. User-Level Systemd (`systemctl --user`) is the standard for Agent-controllable daemons.

The Agent operates as a **Meta-Orchestrator**, driving a logical, topological frontier node-by-node.

## 2. Session Continuity Invariants
Because Agent sessions are ephemeral, the repository must be physically self-describing.
- **`GEMINI.md` (System Prompt Hook)**: Mandated at the repository root. This ensures the Antigravity engine automatically injects the Meta-Orchestrator persona.
- **`artifacts/frontier_state.md` (Macro-State)**: Mandated to track topological nodes, execution status, and feedforward invariants (knowledge required for the next node).
- **Episodic State (`task.md`)**: Strictly *optional*. Local checklist tracking in the episodic brain cache must not be relied upon for session continuity. Micro-state is deferred to GitHub Issues.

## 3. GitHub Issues as the Flow-State Ledger
GitHub Issues act as the primary operational anchor bridging the Human Operator and the Agent. We employ a **Hybrid Epic-Ledger Approach** (see `WHY-0001`):

### 3.1 The Epic Meta-Index (Macro-Ledger)
For every overarching project goal, a single long-lived "Epic" Issue exists. It acts as the cloud-hosted `frontier_state.md`. Its body contains a Meta-Index tracking all completed and active Topological Nodes.

### 3.2 The Node Transactions (Micro-Ledger)
For every discrete Topological Node, a new specific GH-Issue exists. 
- **Contract of Execution**: It defines the strict Scope and Acceptance Criteria (The "Plan") before execution begins.
- **Constraint Injector (HITL)**: The Operator injects feedback directly into the Node Issue's comment thread.
- **Immutability:** Once complete, its Issue is closed, turning it into an immutable transaction log.

## 4. The Materialization Boundary (Side-Bar Rubrics)
To balance flow-state strictness with rapid, low-friction brainstorming, Agents must adhere to the **Materialization Boundary**.

**Permitted Side-Bars (No GH-Issue Required):**
1. **Investigatory / Evaluative Intent:** The Operator asks to "evaluate," "explain," "assess," or "brainstorm" without commanding a state mutation.
2. **Trivially Simple Execution:** One-off operational commands (e.g., `commit and push`).
3. **Information Retrieval:** Extracting context from the codebase.

**Mandatory Materialization (GH-Issue Required):**
1. **Repository Mutation:** Creating, deleting, or modifying files that affect logic, architecture, or persistent state.
2. **Ambiguity in Implementation:** Complex architecture requiring Operator alignment before execution.
3. **State Transitions:** Advancing the topological frontier.

**The WHY Handoff:** *If an investigatory Side-Bar conversation results in a major architectural decision, the Agent must draft a `WHY-*` document (a Decision Record) to permanently preserve the rationale. Only then may the Agent create the formal GH-Issue to execute the decision.*
