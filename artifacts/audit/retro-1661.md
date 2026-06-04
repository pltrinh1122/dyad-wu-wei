# Retrospective: Node 1661 (Plan)

## 1. Goal
Document the resolution for the `checkout` crash (Issue #1659) and formally complete the Plan phase.

## 2. Execution Summary
- Authored the `1661_plan.md` artifact detailing that the bug was implicitly resolved by PR #1722.
- Created `WHAT-1661-checkout-crash-resolution.md` to satisfy the architectural specification invariant for plan nodes.
- Attempted to `checkout` and encountered a `ValueError` because a local test worktree (`node/1661-test-crash`) was previously created with a non-compliant naming convention.
- Encountered a WIP-N=1 synchronization exception due to the orphaned test worktree locking the global state.

## 3. Failure Analysis
- **Trigger**: Creating a manual worktree `node/test-crash` violated the branch naming standard `node/<id>-<kebab-case>`, raising a `ValueError`.
- **Root Cause**: An operator/agent bypassed the node wrapper scripts (`spao node checkout`) and ran raw test operations that breached the invariants.
- **Remediation**: The invalid test worktree was purged via `git worktree remove --force`, releasing the WIP-N=1 lock and allowing standard synchronization and checkout to proceed.

## 4. Learnings & Invariants
- The system correctly isolates and aborts arbitrary non-compliant test branches from corrupting the overarching execution loop.
- The telemetry daemon traps all uncaught exceptions, meaning even expected validation rejections (like branch naming errors) are formally triaged as system faults. This ensures no failure goes uninvestigated.
