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

A compliant child workspace MUST adopt the following physical layout:

```text
child-workspace/
├── .git/                      # (1) The Project Repository (tracks sovereign artifacts/state)
├── .worktrees/                # (2) Project Worktrees (dynamic node execution branches)
│   └── node-X/
├── artifacts/                 # (3) Sovereign State Memory
└── .dz-cil/                   # (4) The Engine Submodule
    ├── .git                   # (Submodule pointer)
    ├── bin/                   # Engine Entrypoints
    └── kernel/                # Core Orchestration Logic
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

## 4. The Fractal Dao Invariant (Sovereignty vs. Inheritance)

A critical consequence of isolating the engine in a submodule is that the parent's `GEMINI.md` and `kb/` primitives (the "Dao Wisdom") are physically shifted into the `.dz-cil/` subdirectory. 

We initially theorized that the child workspace should sever this inheritance to preserve "Domain Sovereignty" and prevent "Persona Bleed", resulting in a standalone local `GEMINI.md`.

### Falsification of the Sovereign Lobotomy
This theory is catastrophically falsified. If the child workspace operates on a purely standalone `GEMINI.md` and ignores `.dz-cil/kb/`, the Agent entering the child workspace is fundamentally lobotomized. It loses the entire SPAO execution loop, all Universal Invariants, and the Meta-Orchestrator logic. The goal of DZ-CIL is not to build a local script executor, but to deploy the **Meta-Orchestrator** as a fractal methodology across any downstream repository. The Dao is universal; it does not bleed into the domain, it governs it.

### Synthesis (The Projection Sourcing Strategy)
To maintain structural decoupling while ensuring the Agent fully inherits the Dao Wisdom, the child workspace MUST dynamically project the universal Dao into its local root context so the IDE Framework can load it.

1. **Knowledge Base Projection**: The child workspace must project the universal knowledge base into its root via symlink: `kb -> .dz-cil/kb`. This ensures all `WHAT-` and `WHY-` primitives are natively available to the Agent's context resolution.
2. **Dynamic GEMINI Sourcing**: The child's root `GEMINI.md` must act as a dynamic assembly interface. It must natively source the core universal logic from `.dz-cil/GEMINI.md` while appending its own local `artifacts/strategic_intent.yml` (Model 1 Sovereign Intent). This guarantees the Agent operates as the strict Meta-Orchestrator, but bounded by the local repository's specific architectural goals.
