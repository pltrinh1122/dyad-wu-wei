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

## 2. Decision: The Ziran Workspace as a Nested Metasystem

We will not build the Ziran Workspace as a collection of hardcoded, monolithic applications. Instead, the **Ziran Workspace will be designed as a generic, portable, document-centric Metasystem Engine**. 

Under this architecture:
- The Workspace provides the **Ziran** (the core compute substrate, API hooks, and local file loops) for building specific domain apps.
- The Operator uses the workspace's nested DZ-CIL engine to systematically build and shape their specific "domain apps" (e.g., the vacation plan, the serial novel) in the same topological, node-by-node SPAO manner used to build the parent DZ-OS.
- In this model, the *chapters of a novel* or the *logistical steps of a trip* are treated as the "codebase" of the domain app, and writing/planning actions are structured as topological node transactions.

```
┌────────────────────────────────────────────────────────┐
│                   Unified Web UI                       │
│      (Interactive SPAO Visualizer & Editor Panel)       │
└───────────────────────────┬────────────────────────────┘
                            │ (Local API Loops)
                            ▼
┌────────────────────────────────────────────────────────┐
│            Nested Document-SPAO Engine                 │
│  (Backlog Scheduler, Node Lifecycler, Commit States)   │
└───────────────────────────┬────────────────────────────┘
                            │ (Pluggable Rules)
                            ▼
┌────────────────────────────────────────────────────────┐
│              Extensible Verification Hook              │
│  (Pluggable Compilers: Continuity & Logistical Linters)│
└───────────────────────────┬────────────────────────────┘
                            │ (Flat Files)
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Document Substrate                   │
│   (Markdown Outlines + YAML Frontmatter Metadata)      │
└────────────────────────────────────────────────────────┘
```

---

## 3. Core Engine Components

To allow the Operator to build domain apps inside the workspace, the engine will implement four modular components:

### 3.1 The Document Backlog and Node Lifecycler
* **Objective**: Replicate the rigor of SPAO for general text files without Git worktree overhead.
* **Mechanism**: The engine maintains a local `backlog.yml` listing planning goals (Paths) and task checkmarks (Nodes).
* **Transitions**: When the Operator activates a node (e.g., "Draft Chapter 1" or "Verify Hotel Reservations"), the engine locks the node, opens a transient draft buffer (equivalent to checkout), and runs pluggable validation routines before merging the draft into the main project document.

### 3.2 The Pluggable Verification Hook (The Semantic Compiler)
Instead of hardcoding validation rules, the engine exposes a pluggable verification interface where different domain rules can be registered:
* **The Novel Studio Plugin**: A semantic continuity linter. It parses character profiles and timeline metadata inside the frontmatter of Markdown files, flagging logical discrepancies (e.g., character acting after a registered death event, or physical location overlaps).
* **The Travel Planner Plugin**: A logistical check linter. It parses date ranges, transit routes, and packing checklist completion states, flagging backtracking logistics or scheduling overlaps.

### 3.3 The Document Substrate
* **Format**: Flat Markdown files representing the active state of the domain application, using standard YAML frontmatter for structural metadata.
* **Storage**: Stored locally in a dedicated user-defined directory, keeping personal data detached from the development engine.

---

## 4. Portability & Substrate Decoupling

The Ziran Workspace code (the nested SPAO engine, pluggable validation libraries, and local Flask-based UI) will be developed and tested in this repository by the parent DZ-CIL agent. However, the runtime instances of the workspace and the Operator's actual documents (the novels, vacation assets) will reside in the Operator's user space. This maintains a strict boundary between the Metasystem's developmental environment and the Operator's personal work.
