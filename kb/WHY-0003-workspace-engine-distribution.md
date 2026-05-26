# WHY-0003: Orthogonal Peer Topology for Workspace Engine Distribution

## Classification
- **Type**: WHY (Architectural Decision Record)
- **ID**: WHY-0003
- **Author**: frontier (SG-0002)
- **Created**: 2026-05-25 (Node 1081, Path 985)
- **Context**: Resolving state corruption when updating downstream Model 1 sovereign workspaces.

---

## 1. The Context (The Defect)

The parent `agent-antigravity` repository currently tracks both the universal execution engine logic (`kernel/`, `drivers/`, `bin/`) and highly volatile, environment-specific operational state (`artifacts/frontier_state.md`, `artifacts/strategic_intent.yml`) in the exact same Git tree (`main` branch).

When a child workspace (Model 1 Redirection) attempts to pull updates to the engine logic by directly fetching from the upstream `agent-antigravity` remote, it inherently pulls down the upstream's `artifacts/` state memory. This causes a catastrophic topological collision, permanently corrupting the child's own sovereign memory space and triggering "unrelated histories" defects during merge operations.

---

## 2. The Dialectical Evaluation

We evaluated three potential paradigms to resolve this distribution flaw:

1. **Thesis (Git Attributes Merge-Ours)**: Continue direct git pulling, but employ `.gitattributes` to shield the child's `artifacts/` folder from upstream overwrites. *Falsified* due to brittleness and failure to solve the underlying state coupling.
2. **Antithesis (Nested Submodule Worktrees)**: Isolate the engine as a Submodule at `.workspace/`, and create the project's working trees *inside* the submodule directory at `.workspace/.worktrees/`. *Falsified* because nesting project worktrees inside a pure downstream dependency violates Git boundaries (inversion of control) and structurally breaks the engine's internal path resolution (`path_resolver.py`).
3. **Synthesis (Orthogonal Peer Topology)**: Isolate the engine as a pure Submodule, but structurally decouple the Project Worktrees by mounting them at the project root, keeping them physically unentangled from the engine directory.

---

## 3. The Decision: Orthogonal Peer Topology

We have adopted the **Orthogonal Peer Topology (The Synthesis)** as the canonical architecture for all Model 1 Sovereign Workspaces.

### 3.1 Structural Blueprint

A compliant child workspace MUST adopt the following physical layout to achieve both separation of execution state and Dual-Context resolution of the Dao:

```text
child-workspace/
├── .git/                      # (1) The Project Repository
├── .worktrees/                # (2) Project Worktrees (dynamic node execution branches)
│   └── node-X/
├── artifacts/                 # (3) Sovereign State Memory
├── kb/                        # (4) Sovereign Dao Subclass (Local WHY/WHAT Overrides)
├── GEMINI.md                  # (5) Sovereign Dao Persona (Model 1 Rules)
└── .dz-cil/                   # (6) The Engine Submodule (Universal Base Class)
    ├── .git                   # (Submodule pointer)
    ├── bin/                   # Engine Entrypoints
    ├── kernel/                # Core Orchestration Logic
    ├── kb/                    # Universal Dao Primitives
    └── GEMINI.md              # Universal Dao Persona
```

### 3.2 Key Invariants

1. **Submodule Isolation**: The `agent-antigravity` engine MUST be mounted exclusively as a Git Submodule (typically at `.dz-cil/`). The child project must never directly clone or merge the parent's history into its own root git tree.
2. **Root Worktree Projection**: The Engine's SPAO checkout routines (`bin/node checkout`) MUST project the dynamically created worktrees into the *Project Root* (`.worktrees/`), not inside the engine submodule's directory. 
3. **Zero Engine Refactoring**: This topology requires zero modifications to the universal engine. The engine natively infers the `SPAO_WORKSPACE_DIR` from the execution context and provisions `.worktrees/` exactly where required.

### 3.3 Operator Execution Flow

To update the engine, the Operator simply navigates into the isolated submodule and pulls the latest upstream logic without any risk of polluting the parent project's state:

```bash
# Safely pull the latest engine logic
cd .dz-cil/
git checkout main
git pull origin main

# Execute orchestrator commands normally from the project root
cd ..
./.dz-cil/bin/node status
```

## 4. The Fractal Dao Invariant (Extend and Override)

A critical consequence of isolating the engine in a submodule is that the parent's `GEMINI.md` and `kb/` primitives (the "Dao Wisdom") are physically shifted into the `.dz-cil/` subdirectory. 

We initially theorized that the child workspace could inherit this wisdom via a direct symlink (`kb -> .dz-cil/kb`).

### Falsification of the Symlink Projection
The symlink projection is catastrophically falsified because it destroys the **Extend and Override** inheritance model. A symlink is a strict physical alias. If the child workspace needs to *extend* the Dao with a local primitive (e.g., a custom `WHY-` document for its specific domain architecture) or *override* a universal rule, writing to the symlink will mutate the `.dz-cil/kb/` submodule directly. This pollutes the universal engine state and violates the Submodule Isolation Invariant. The child must be able to hold sovereign knowledge without modifying the parent.

### Synthesis (Dual-Context Resolution)
To maintain both structural decoupling and Dao inheritance, the architecture relies on **Dual-Context Resolution** (The Object-Oriented "Extend and Override" paradigm):

1. **Physical Decoupling**: The child workspace maintains its own standard, standalone `kb/` directory and `GEMINI.md` file in its root. There are no symlinks.
2. **Universal Base Class**: The Agent treats `.dz-cil/kb/` and `.dz-cil/GEMINI.md` as the immutable, inherited Universal Base Class.
3. **Sovereign Subclass**: The local `kb/` and local `GEMINI.md` act as the Sovereign Subclass. The Agent natively loads the universal primitives first, then applies the local primitives. If a conflict exists, the local workspace explicitly overrides the universal engine. All new domain insights are written exclusively to the local `kb/`.
4. **Bootstrapping**: The Agent's IDE framework or internal prompt injection seamlessly merges these dual contexts, allowing the Meta-Orchestrator persona to scale fractally into the child domain without logic bleed or state corruption.
