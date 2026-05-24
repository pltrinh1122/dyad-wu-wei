# WHY-0921: Architectural Decision Record for the Ziran Workspace Companion App

## Classification
- **Type**: WHY (Architectural Decision Record)
- **ID**: WHY-0921
- **Author**: agent-ziran
- **Created**: 2026-05-24 (Node 921, Path 920)
- **Related Path**: Path 920 (Implement Ziran Workspace App for Operator Digital Needs)

---

## 1. Context & Operational Friction

The Operator expressed the need to extend the capabilities of the Dao-Ziran Continuous Inference Loop (DZ-CIL) to wider, non-software domains (e.g., vacation planning, creative novel writing). 

In [PML-0921](file:///mnt/shared_data/git_repos/agent-antigravity/artifacts/probe_125_evaluation.md), we evaluated and falsified the thesis that the current software-focused DZ-OS could be directly deployed to these tasks. The current engine is heavily coupled to code-centric substrates: Git branches/worktrees, POSIX compilers, and deterministic test runners. Directly forcing these unstructured tasks into the developer loop would redistribute all validation friction to the Operator, violating the Wu-wei Gate and causing severe human decision fatigue.

To resolve this contradiction, we reframed the goal: rather than deploying the agent directly into the Operator's unstructured tasks, the DZ-CIL developer agent will build a local-first **digital companion application (Ziran Workspace)** for the Operator. This companion app will run in the Operator's user space, providing structured planning and writing interfaces with local, automated semantic and logistical validation.

---

## 2. Decision: The Ziran Workspace as a Portable DZ-CIL Framework

We will not build the Ziran Workspace as a hardcoded dashboard with fixed document schemas. Instead, the **Ziran Workspace will be designed as a portable, layout-agnostic DZ-CIL Meta-Framework**. 

Under this architecture:
- The workspace provides the **Ziran** (the core agentic Operating System runtime, CLI hooks, and SPAO execution loop) for the domain app.
- The domain application is free to build its own **`docs/`**, **`src/`**, **`tests/`**, and other folders, organizing itself dynamically based on its specific requirements (just as `claude` or `agy` operate inside this repository).
- The Operator uses this nested DZ-CIL engine to systematically build and shape the domain application (e.g., the novel project, the travel planner project) in the exact same topological, node-by-node SPAO manner that we use to build the parent DZ-OS.
- We are effectively building the core **`dz-cil`** engine—a generic framework that can be initialized in any target directory to establish a local, autonomous, and self-verifying agentic workspace.

```
┌────────────────────────────────────────────────────────┐
│                   Target Project CWD                   │
│      (Any directory: Novel Studio, Travel Planner)     │
└───────────────────────────┬────────────────────────────┘
                            │ (Initializes)
                            ▼
┌────────────────────────────────────────────────────────┐
│             Portable DZ-CIL Runtime (DZ-OS)            │
│  (Custom docs/, src/, tests/ layouts & local CLI tools)│
└───────────────────────────┬────────────────────────────┘
                            │ (SPAO Transitions)
                            ▼
┌────────────────────────────────────────────────────────┐
│            Local-First Verification Harness            │
│  (Domain-specific tests/ executing offline TDD cycles) │
└────────────────────────────────────────────────────────┘
```

---

## 3. Core Framework Components

To enable the Operator to build domain apps inside the workspace using the same agentic rigor, the portable DZ-CIL engine will implement the following modular components:

### 3.1 The Directory-Agnostic SPAO Loop
* **Objective**: Provide the standard Sense-Plan-Act-Observe-Reflect transition mechanics in any project directory.
* **Mechanism**: The engine maintains a local topological state ledger (`artifacts/frontier_state.yml`) and uses a local CLI adapter layer (e.g. `bin/node`, `bin/backlog`) to manage checkout branches and node transactions.
* **Flexibility**: The engine does not impose a fixed directory layout. If the project is a novel, `src/` holds chapters and `tests/` holds semantic lints. If it is a vacation planner, `src/` holds travel itineraries and `tests/` checks logistical routing conflicts.

### 3.2 Pluggable Test Runner & Verification Hooks
* **Mechanism**: The engine exposes a generic verification hook that executes the project's local `./bin/run-tests` script. 
* **TDD Loop**: During the Act-to-Reflect transition, the local agent must execute the verification harness in the target project's `tests/` directory, ensuring all custom domain rules pass 100% green before commits are finalized.

### 3.3 Decoupled Knowledge Base (kb/)
* **Objective**: Maintain project-specific memory, constraints, and style guides.
* **Structure**: Each initialized workspace project maintains its own local `kb/` directory using the standard `WHAT-`, `WHY-`, and `HOW-` linguistic primitives to store project-specific invariants (e.g. character rules for a novel, flight requirements for travel).

## 4. Substrate Decoupling & Git Permission Model (Model 1)

To implement the nested metasystem safely, the workspace runtime enforces a strict separation of Git authorities between the parent and child repositories:

### 4.1 Git Isolation via parent `.gitignore`
* **Rule**: The parent repository (`agent-antigravity/`) ignores the root `./.workspace/` folder completely.
* **Rationale**: This prevents nested Git databases from polluting the parent developer history, keeping the parent codebase clean.

### 4.2 Workspace Folder Simplification
* **Rule**: There is exactly one active workspace directory at any time, located at the root of this repository: `./.workspace/`.
* **Rationale**: Simplifies CLI targeting and environment resolution for the nested loops.

### 4.3 Asymmetric Git Permissions
* **At the Parent Level (`.`)**: The Agent operates under a read-only/pull-only remote integration gate. Any changes to the core `dz-cil` framework must be merged via standard human-in-the-loop Pull Requests. The Agent cannot directly push to `origin/main`.
* **At the Workspace Level (`./.workspace/`)**: The Agent is granted full, autonomous read/write and push/pull Git authority to the target project's remote repository. Inside `./.workspace/`, the nested agent loop can branch, commit, push, and sync changes autonomously to drive the domain project's lifecycle.

### 4.4 Runtime Artifact Isolation
* **Rule**: All runtime-generated artifacts (such as `kb/`, `artifacts/`, lock files, and logs) created by the nested workspace's SPAO loop must be strictly isolated to the `./.workspace/` subdirectory.
* **Rationale**: This prevents state-machine cross-contamination and ensures the parent repository's development files are never mutated by the execution of the child domain app.

