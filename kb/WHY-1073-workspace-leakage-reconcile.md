# WHY-1073: Prevention of Parent Metadata Leakage in Reflection

## Classification
- **Type**: WHY (Decision Rationale)
- **ID**: WHY-1073
- **Author**: agent-sg5
- **Created**: 2026-05-27 (Node 1073, Path 985)

---

## 1. Context
During the reflect phase inside a child workspace, copying tracking state files (`frontier_state.*`) from the root directory into the active worktree caused directory dirtiness and state inconsistencies.

## 2. Decision
To resolve this, we mandate that:
1. State mutation during checkout and reflect must execute entirely inline inside the worktree checkout directory.
2. The orchestrator must not copy parent tracking files down to child workspaces, preventing parent metadata leakage.
