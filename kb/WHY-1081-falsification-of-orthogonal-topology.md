# WHY-1081: Falsification of Orthogonal Peer Topology (Reaffirmation of Model 1)

## Classification
- **Type**: WHY (Architectural Decision Record - Falsification)
- **ID**: WHY-1081
- **Author**: frontier (SG-0002)
- **Created**: 2026-05-25 (Node 1081, Path 985)
- **Context**: Resolving state corruption when updating downstream Model 1 sovereign workspaces.

---

## 1. The Context (The Defect)

A defect was observed where a child workspace suffered state corruption because pulling upstream Engine updates caused merge conflicts in the `artifacts/` directory. We incorrectly assumed this was a structural flaw in the Model 1 architecture (`WHY-0921`) and attempted to invent a new "Orthogonal Peer Topology" where the project is the root and the engine is mounted as a `.dz-cil/` submodule.

---

## 2. The Dialectical Evaluation (The Failed Experiment)

We evaluated the Orthogonal Peer Topology through a series of dialectical stress tests. It systematically failed every foundational invariant of the DZ-CIL Dao:

1. **Loss of Dao Inheritance (The Lobotomy)**: By moving the engine to a submodule, the parent's `GEMINI.md` and `kb/` are hidden from the IDE's root context. The Agent entering the workspace is lobotomized, losing the Meta-Orchestrator persona and the SPAO execution loop.
2. **Failure of Extend and Override**: Attempts to restore the Dao via symlinks (`kb -> .dz-cil/kb`) catastrophically failed because a symlink prevents the child from *extending* the knowledge base without polluting the universal engine state.
3. **Loss of Engine Immutability**: If the child is the root, the architecture implies the child can extend or override the execution wrappers (`bin/`) and logic (`kernel/`). This destroys the universality of the SPAO Engine and reverts the environment to chaotic scripting.
4. **Specification Collapse**: The Orthogonal Peer Topology inherently contradicts the explicitly defined and proven architecture in `WHY-0921` and `WHAT-0930`, requiring a massive rewriting of the system's foundational specifications.

---

## 3. The Synthesis (Reaffirming WHY-0921)

The "Orthogonal Peer Topology" is entirely falsified. 

The original defect (state corruption during `git pull`) was not caused by a flaw in Model 1. It was caused by the Operator deploying the child workspace (`dz-ta`) as a direct clone/fork of the engine, rather than using the correct `bin/workspace init` installer defined in `WHAT-0930`. By cloning the engine directly, the child inherited the engine's physical `artifacts/` Git tracking, causing collisions.

### The True Resolution
1. **Strict Adherence to Model 1**: The Engine MUST remain the Root Parent repository (`DZ-CIL_ROOT`). The Child Workspace MUST be nested inside the parent at `./.workspace/` as defined in `WHY-0921`.
2. **Native Dao Inheritance**: Because the IDE opens at the Engine Root, the Agent natively inherits the Universal Dao (`kb/` and `GEMINI.md`). The Agent then natively applies the "Extend and Override" paradigm by merging the child's `SPAO_WORKSPACE_DIR/GEMINI.md` and operating on the nested `SPAO_WORKSPACE_DIR`.
3. **Immutable Engine**: The Engine (`bin/`, `kernel/`) remains securely at the root, immutable to the child, enforcing the Laws of Physics across any domain application placed in `.workspace/`.

**Conclusion**: Node 1081 serves as the definitive dialectical proof that the Model 1 Nested Workspace architecture (`WHY-0921`) is structurally perfect and must not be inverted. All attempts to invert the Engine-Workspace relationship lead to catastrophic systemic collapse.
