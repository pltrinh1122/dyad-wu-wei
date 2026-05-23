# WHY-0034: Three-Loop Governance Framework Alignment

This document outlines the architectural and operational breakdown of the Three-Loop Project Governance Framework within the `agent-antigravity` context. 

## Context & Objectives

The operator is catching this agent up to the Three-Loop Project Governance Framework. Since this agent only manages the SPAO framework itself, we only operate within **SPAO** and **SDLC** loops.

We break the briefing concepts down into five orthogonal units to seek clarification and establish the boundary invariants before plan execution.

---

## 1. Orthogonal Concept Breakdown & Operator Decisions

### Concept A: Sibling Loops & Boundary Transitions (SPAO vs. SDLC)
* **Ontology**: Direct updates to the repository laws and documentation (`kb/`, `artifacts/`, rules, workflows) are **SPAO** events. System software changes (Python files, CLI wrappers, testing fixtures) are **SDLC** events.
* **Operator Decisions**:
  - **A1**: Yes, the `loop:spao` and `loop:sdlc` classifications (along with `area:*` and `kind:*`) must be formally registered as issue labels on GitHub and tracked in the local `artifacts/frontier_state.yml`.
  - **A2**: Yes, new Execute Activities should be appended/amended to the Path. Execute Activities must use the same standard backlog issue template as other nodes (Refine, Plan, Reflect).

### Concept B: SPEC Handoff / Plan Invariants (Gate-1 & Gate-2)
* **Ontology**: In our system, the SPEC maps to the `WHAT-` specification document and the `implementation_plan.md` artifact.
  - **Gate-1 (Planning Accept)**: The operator approves the plan.
  - **Gate-2 (Execution Accept)**: The agent confirms the plan is implementable.
* **Operator Decisions**:
  - **B1**: Yes, explicitly represent Gate-1 and Gate-2 as checkbox invariants in our `task.md` and planning templates.
  - **B2**: Yes, `spao node plan-finish` must check and block execution if a corresponding `WHAT-` spec file is not tracked in the `kb/` directory.

### Concept C: Branch Model per Loop
* **Ontology**: Both SPAO and SDLC loops in this project target the `main` branch.
* **Operator Decisions**:
  - **C1 (Worktree Separation)**: Option B (partitioned `.worktrees/spao/` vs `.worktrees/sdlc/` directories) was selected.
  - **C2 (PR Purity Verification)**: Make the PR file-purity check/enforcement configurable for SPAO (e.g. in `antigravity.yml`).

### Concept D: Universal Merge Gate (HTIL)
* **Ontology**: Merging to the target branch is the universal Human-Touch-in-Loop (HTIL) gate.
* **Operator Decisions**:
  - **D1**: Yes, `spao node reflect` must summarize loop transitions and identify observed variances along with recommendations in the generated PR description to facilitate SDLC loop improvement.

### Concept E: Orthogonal Label Dimensions
* **Ontology**: Classification along three independent axes: `area:*`, `loop:*`, `kind:*`.
* **Operator Decisions**:
  - **E1**: Metadata dimensions will live as GitHub issue labels and be synchronized/tracked in the local `frontier_state.yml` node items.

---

## 2. Concept C1: Worktree Separation Trade-offs

The operator must select between two directory layouts for local checkouts:

### Option A: Shared `.worktrees/node/<branch-name>` (Status Quo)
* **Pros**: Simple, zero change to existing path resolvers, git wrappers, or setup scripts. Keeps all active checkouts under one standard directory.
* **Cons**: No structural or visual separation of SPAO (policy) worktrees from SDLC (code) worktrees.

### Option B: Partitioned `.worktrees/spao/<branch-name>` vs `.worktrees/sdlc/<branch-name>`
* **Pros**: Filesystem layout mirrors the loop ontology. Easy to clean up code checkouts while preserving policy documentation workspaces. Loop context is instantly visible from path string.
* **Cons**: Requires refactoring `drivers/path_resolver.py` and `kernel/node_lifecycle.py` to route paths dynamically based on node metadata labels.

---

## 3. Concept F: Loop Mechanics and States

To prevent structural confusion, the operational mechanics and states are defined below:

### 3.1 SPAO Loop (Outer Governance)
* **Role**: Governs the project itself, its policies, knowledge base, taxonomy, and system constraints.
* **Target Workspace Files**: `kb/*` (rules/GLOSSARY), `artifacts/*` (state trackers/ledgers), `GEMINI.md`.
* **Transitions**: Mediates all transitions between loops and registers path updates.
* **States**:
  1. **Align (Probe)**: Resolves philosophical and technical intent. Outputs: `kb/WHY-*.md` document.
  2. **Plan (Probe)**: Captures planning intent and constraints. Outputs: `kb/WHAT-*.md` and backlog task items.
  3. **Reflect (Activity)**: Integrates policy modifications. Outputs: Updated trackers and merged PR.

### 3.2 SDLC Loop (Inner Software Development)
* **Role**: Implements software specifications, compiles code, runs test suites, and provisions tools.
* **Target Workspace Files**: `bin/*`, `kernel/*`, `drivers/*`, `tests/*`, `infra/*`.
* **Transitions**: Cross-loop dependencies are registered in the SPAO work-graph. SDLC consumes SPECs produced in SPAO.
* **States**:
  1. **Align (Probe)**: Clarifies interface boundaries and software requirements. Outputs: `kb/WHY-*.md` design record.
  2. **Plan (Probe)**: Finalizes the software design and specification. Outputs: `kb/WHAT-*.md` spec, `implementation_plan.md`, and Gate-1 & Gate-2 checklists.
  3. **Act (Execute Activity)**: Performs actual code modification. Outputs: Commits and tests in the worktree.
  4. **Reflect (Reflect Activity)**: Verifies software correctness. Outputs: `walkthrough.md` test metrics, PR with observed loop variances and recommendations, and HTIL merge trigger.
