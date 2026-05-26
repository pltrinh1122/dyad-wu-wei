# WHAT-0935: ISBO Ontology and Architecture

## Classification
- **Type**: WHAT (Technical Specification / Ontology)
- **ID**: WHAT-0935
- **Author**: agent-frontier
- **Created**: 2026-05-26
- **Implements decisions from**: WHY-0935

---

### 1. The ISBO Ontology

The **ISBO** framework defines the four mutually exclusive, sequential phases required for a Disciple (or the Creator) to stand up a new autonomous application using the DZ-CIL engine. It is a strict discipline designed to isolate the Engine from the Domain.

#### Phase 1: [I]nstall (Procurement of the Engine)
- **Definition**: The physical acquisition of the Meta-Orchestrator engine (`agent-antigravity`). This is the procurement of the loom, not the weaving of the fabric.
- **State Condition**: The Operator's machine possesses a local clone of the DZ-CIL engine repository. 
- **Actor**: The Operator acting as a Systems Administrator.
- **Artifact**: A local directory containing the Dao-Ziran laws and execution engine (e.g., `/mnt/shared_data/git_repos/agent-antigravity`).

#### Phase 2: [S]etup (Provisioning the Sovereign Domain)
- **Definition**: The generation of a mathematically isolated child workspace. This establishes the physical boundary protecting *Wu-wei*.
- **State Condition**: The physical directory structure, empty `kb/` and `artifacts/` pillars, virtual environments, and `.gitignore` mappings are created, physically decoupled from the Engine.
- **Actor**: The DZ-CIL Engine executing `bin/workspace init` on behalf of the Operator.
- **Artifact**: A pristine, sovereign Model 1 Workspace directory (e.g., `/mnt/shared_data/dzw/dz-ta`).

#### Phase 3: [B]ootstrap (Injection of the Telos)
- **Definition**: The injection of the Creator/Disciple's specific domain Telos into the empty workspace. An agent cannot act without intent.
- **State Condition**: The Agent captures the unformed intent of the Operator and codifies it into the absolute North Star document.
- **Actor**: The Agent, guided by the Operator in the sovereign terminal.
- **Artifact**: The materialization of `artifacts/strategic_intent.yml` within the child workspace, anchoring the system to a distinct goal.

#### Phase 4: [O]perate (Continuous Execution)
- **Definition**: The transition into the standard Dao-Ziran Continuous Inference Loop (DZ-CIL).
- **State Condition**: The Agent enters the SPAO loop (Sense-Plan-Act-Observe) against the populated Strategic Intent, generating backlog Nodes and executing against the domain logic.
- **Actor**: The Dual-Agent (The autonomous Agent proposing action + The Operator providing HITL approvals as the Director).
- **Artifact**: Execution of standard Path and Node abstractions, tracked via the child's `frontier_state.md`.

### 2. The Isolation Boundary
ISBO mathematically separates the "Engine Room" (Install) from the "Domain Workspace" (Setup -> Operate). The Engine is a generic utility providing the laws of physics; the Domain is the sovereign instantiation where the Disciple applies those laws to a specific problem.
