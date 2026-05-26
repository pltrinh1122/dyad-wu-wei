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
└── .workspace/                # (4) The Engine Submodule
    ├── .git                   # (Submodule pointer)
    ├── bin/                   # Engine Entrypoints
    └── kernel/                # Core Orchestration Logic
```

### 3.2 Key Invariants

1. **Submodule Isolation**: The `agent-antigravity` engine MUST be mounted exclusively as a Git Submodule (typically at `.workspace/` or `.engine/`). The child project must never directly clone or merge the parent's history into its own root git tree.
2. **Root Worktree Projection**: The Engine's SPAO checkout routines (`bin/node checkout`) MUST project the dynamically created worktrees into the *Project Root* (`.worktrees/`), not inside the engine submodule's directory. 
3. **Zero Engine Refactoring**: This topology requires zero modifications to the universal engine. The engine natively infers the `SPAO_WORKSPACE_DIR` from the execution context and provisions `.worktrees/` exactly where required.

### 3.3 Operator Execution Flow

To update the engine, the Operator simply navigates into the isolated submodule and pulls the latest upstream logic without any risk of polluting the parent project's state:

```bash
# Safely pull the latest engine logic
cd .workspace/
git checkout main
git pull origin main

# Execute orchestrator commands normally from the project root
cd ..
./.workspace/bin/node status
```

## 4. The Domain Sovereignty Invariant (GEMINI.md Decoupling)

A consequence of isolating the engine in a submodule is that the parent's `GEMINI.md` file (which contains the Agentic Core Loop instructions) is physically hidden from the root of the child workspace. 

We explicitly **reject** the proposition that the child workspace's `GEMINI.md` should automatically "source" or concatenate the parent's `GEMINI.md`.

### Falsification of Auto-Sourcing
If the child workspace blindly inherits the parent's `GEMINI.md`, the child agent will suffer severe cognitive dissonance:
1. **Persona Bleed**: The parent's `GEMINI.md` establishes the "Meta-Orchestrator" or "Frontier Agent" persona, which is mathematically tasked with *modifying the execution engine itself* (e.g., maintaining `kernel/` and `drivers/`). The child workspace agent is a downstream user of the engine, tasked with building a specific application (`dz-ta`). 
2. **Path Hallucinations**: Sourcing the parent's rules would command the child agent to obey constraints (like the `drivers/` vs `kernel/` architectural boundary) on folders that don't exist in its local repository, leading to immediate execution paralysis.

**The Solution:** The child workspace MUST define its own sovereign, standalone `GEMINI.md` (The "Model 1" Persona) that sets rules for its specific application domain. The universal system invariants (e.g., TDD, SPAO loop logic) are enforced *natively by the executables* (`./.workspace/bin/node`), not through raw text prompts. The agent trusts the engine's gates, rather than reading the engine's source code rules.
