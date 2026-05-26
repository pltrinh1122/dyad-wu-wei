# WHY-1121: Architectural Decisions for ISBO Completeness

## Context
Path 1119 (Achieve ISBO Completeness) requires laying out the end-to-end framework of the Install-Setup-Bootstrap-Operate lifecycle. We must mathematically prevent the conflation of the "Creator" (Engine Architect) and "Director" (Domain Operator) roles.

## Decisions

### 1. Pure Isolation of Setup (Node 1066)
We decide to refactor `bin/workspace` to avoid copying the entire engine logic into the child workspace. A workspace setup is a clean provision of directory structures and symbolic links back to the parent engine wrappers. This preserves dry, single-source engine maintenance and avoids workspace git leakage.

### 2. The Blocking Bootstrap Invariant (Node 1123)
On agent startup inside a child workspace, if `artifacts/strategic_intent.yml` is not found, the agent must enter a hard block. It cannot run any tasks, plan any nodes, or execute status checks. The agent must prompt the user to input their unformed intent and generate `strategic_intent.yml` first.

### 3. Dual-Backlog Routing (Node 1124)
When operating inside a child workspace context, backlog operations must be routed strictly relative to `SPAO_WORKSPACE_DIR` if set. This shields the parent meta-backlog from child domain pollution, and ensures child nodes are managed within the child workspace.

## Invariants
- **Bootstrapping Invariant**: The agent strictly requires a `strategic_intent.yml` before entering the Operate phase in a child workspace.
- **Workspace Edit Boundary**: Child workspaces are sovereign and decoupled from the parent engine repository.
