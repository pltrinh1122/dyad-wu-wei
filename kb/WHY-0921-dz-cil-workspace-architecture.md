# WHY-0921: Architectural Decision Record for the DZ-CIL Workspace

## Classification
- **Type**: WHY (Architectural Decision Record)
- **ID**: WHY-0921
- **Author**: agent-ziran
- **Created**: 2026-05-24 (Node 921, Path 920)
- **Related Path**: Path 920 (Implement DZ-CIL Workspace for Operator Digital Needs)

---

### 1. Context & Operational Friction

The Operator expressed the need to extend the capabilities of the Dao-Ziran Continuous Inference Loop (DZ-CIL) to wider, non-software domains (e.g., vacation planning, creative novel writing). 

In [PML-0921](file:///mnt/shared_data/git_repos/dz-cil/artifacts/probe_125_evaluation.md), we evaluated and falsified the thesis that the current software-focused DZ-OS could be directly deployed to these tasks because it is heavily coupled to Git databases and local code compilers. Directly forcing these unstructured tasks into the parent developer loop would redistribute all validation friction to the Operator, violating the Wu-wei Gate and causing severe human decision fatigue.

To resolve this contradiction, we reframe the architecture around **Model 1 (Dual-Context Workspace)**. Under Model 1, the parent agent runs from the root of the parent repository (`DZ-CIL_ROOT` or `.`) but is granted filesystem permissions to access and operate on the nested project repository located at `./.workspace/`. The Agent possesses dual context: it knows the metasystem rules of the parent `dz-cil` engine and actively executes the backlog and node lifecycle transactions directly in the child `project` repository.

---

## 2. Decision: The DZ-CIL Workspace as a Dual-Context Metasystem (Model 1)

We will design and build the DZ-CIL Workspace as a **Model 1 Dual-Context agentic execution loop**. 

Under this architecture:
- The workspace engine (the CLI wrappers, kernel daemons, and drivers) remains located solely in the parent repository (`DZ-CIL_ROOT` or `.`). No duplicate `dz-cil` orchestrators or kernel scripts are copied to the child project.
- The target project is checked out inside the `./.workspace/` directory and is free to build its own **`docs/`**, **`src/`**, **`tests/`**, and other folders, organizing itself dynamically based on its domain requirements (just as `claude` or `agy` do in their respective workspaces).
- The Operator uses the parent DZ-CIL engine to systematically build and shape the domain application (e.g. drafting chapters, planning flight legs) in the exact same topological, node-by-node SPAO manner used to build the parent DZ-OS.
- When the Operator activates a workspace path/node, the parent agent's logic executes the lifecycle transitions (checkout, plan, test, reflect) by targeting the `./.workspace/` directory.

```
┌────────────────────────────────────────────────────────┐
│             Parent DZ-CIL Engine (at .)                │
│    (Core Orchestration, CLI wrappers, Git drivers)     │
└───────────────────────────┬────────────────────────────┘
                            │ (Orchestrates / Operates)
                            ▼
┌────────────────────────────────────────────────────────┐
│             Nested Project Workspace (Model 1)         │
│          Located at root CWD: ./.workspace/            │
│  (Custom docs/, src/, tests/ layouts & local Git repo) │
└───────────────────────────┬────────────────────────────┘
                            │ (Runs TDD Loops)
                            ▼
┌────────────────────────────────────────────────────────┐
│            Local-First Verification Harness            │
│  (Domain-specific tests/ executing offline TDD cycles) │
└────────────────────────────────────────────────────────┘
```

---

## 3. Core Framework Components

To enable the parent agent to orchestrate the nested workspace project under Model 1, the engine will implement the following modular components:

### 3.1 The Directory-Targeted SPAO Loop
* **Objective**: Run the Sense-Plan-Act-Observe-Reflect transition mechanics targeting the `./.workspace/` directory.
* **Mechanism**: The parent CLI adapters (e.g. `bin/node`, `bin/backlog`) execute the state transitions (like checkouts and reflections) by targeting the nested child Git repository, utilizing parent-level drivers but pointing them to the target subdirectory.
* **Flexibility**: The engine does not impose a directory layout on the child project. If the project is a novel, `src/` holds chapters and `tests/` holds semantic lints. If it is a vacation planner, `src/` holds travel itineraries and `tests/` checks logistical routing conflicts.

### 3.2 Pluggable Test Runner & Verification Hooks
* **Mechanism**: The parent engine executes verification hooks by running the project's local `./bin/run-tests` script inside the target `./.workspace/` directory.
* **TDD Loop**: During the Act-to-Reflect transition, the local agent must execute the verification harness in the target project's `./.workspace/tests/` directory, ensuring all custom domain rules pass 100% green before commits are finalized.

### 3.3 Decoupled Workspace Knowledge Base
* **Objective**: Maintain project-specific memory, constraints, and style guides.
* **Structure**: The nested project maintains its own local `./.workspace/kb/` directory using standard `WHAT-`, `WHY-`, and `HOW-` linguistic primitives to store project-specific invariants (e.g. character sheets for a novel, flight parameters for travel).

---

## 4. Substrate Decoupling & Git Permission Model (Model 1)

To implement the nested metasystem safely, the workspace runtime enforces a strict separation of Git authorities and workspace artifacts:

### 4.1 Git Isolation via parent `.gitignore`
* **Rule**: The parent repository (`DZ-CIL_ROOT`) ignores the root `./.workspace/` folder completely.
* **Rationale**: This prevents nested Git databases from polluting the parent developer history, keeping the parent codebase clean.

### 4.2 Workspace Folder Simplification
* **Rule**: There is exactly one active workspace directory at any time, located at the root of this repository: `./.workspace/`.
* **Rationale**: Simplifies CLI targeting and environment resolution for the nested loops.

### 4.3 Asymmetric Git Permissions
* **At the Parent Level (`.`)**: The Agent operates under a read-only/pull-only remote integration gate. Any changes to the core `dz-cil` framework must be merged via standard human-in-the-loop Pull Requests. The Agent cannot directly push to `origin/main`.
* **At the Workspace Level (`./.workspace/`)**: The Agent is granted full, autonomous read/write and push/pull Git authority to the target project's remote repository. Inside `./.workspace/`, the nested agent loop can branch, commit, push, and sync changes autonomously to drive the domain project's lifecycle.

### 4.4 Runtime Artifact Isolation
* **Rule**: All runtime-generated artifacts (such as `kb/`, `artifacts/`, lock files, and logs) created by the nested workspace's SPAO loop must be strictly isolated to the `./.workspace/` subdirectory.
* **Rationale**: This prevents state-machine cross-contamination and ensures the parent repository's development files (such as `artifacts/frontier_state.md` and lock files) are never mutated by the execution of the child domain app.
