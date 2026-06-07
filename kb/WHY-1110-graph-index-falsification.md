# WHY-1110: Architectural Falsification of Static Graph Index

> [!NOTE]
> **Status**: Finalized  
> **Node**: 1110 (Probe — Path 769)  
> **Persona**: agent-sg5 (SG-0005: Autonomous Knowledge Accrual)  
> **Date**: 2026-06-06

## 1. Intent
To investigate the feasibility of a lightweight `kb/graph_index.yml` adjacency index auto-updated during `plan-finish`, alongside a `kb graph` CLI command for structured neighbor traversal. 

## 2. Dialectical Falsification: The State Synchronization Mismatch
The thesis of updating `kb/graph_index.yml` during the `plan-finish` phase is fundamentally falsified due to a dual invariant collision:
1. **The PR Discipline Invariant (WHAT-0010)**: The `kb/` directory is the canonical ROM/Dao of the system. Mutating a file in `kb/` on the `main` branch directly via the `plan-finish` orchestrator violates the invariant that no codebase mutations occur outside of a tested Pull Request.
2. **Worktree Inheritance Isolation**: `plan-finish` operates on the local `main` branch before a worktree is created. When `checkout` executes, it clones the worktree from `origin/main` and strategically inherits *only* `artifacts/frontier_state.*` to prevent state leakage. Uncommitted updates to `kb/graph_index.yml` on `main` are inherently orphaned, invisible to the newly instantiated Act-phase worktree. 

This confirms the conditionally identified F1 — Retrieval Architecture Mismatch.

## 3. Resolution & Feasibility
While the static, auto-updated `graph_index.yml` is structurally rejected, the requirement for a machine-queryable graph to improve inferencing remains valid. 
A stateless `bin/kb graph` CLI tool that parses markdown headers dynamically at query time satisfies the requirement without maintaining fragile state.

### Result
- The static `kb/graph_index.yml` index update via `plan-finish` is formally rejected.
- A downstream Activity node has been spawned to implement the stateless `bin/kb graph` CLI parser.
