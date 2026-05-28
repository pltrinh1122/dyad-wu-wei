# WHY-0035: Git Transaction Ownership by SPAO

This document outlines the architectural and operational alignment for git transaction ownership within the SPAO loop.

## Context & Objectives

Currently, when the builder agent completes an implementation in a partitioned worktree, they might manually invoke `git-add`, `git-commit`, and `git-push` inside the worktree. This manual staging pre-empts the atomic transaction managed by `spao node reflect`, meaning:
1. **Pre-empted Rollbacks**: If subsequent reflection steps (like GitHub PR creation or meta-index checkoffs) fail, the transaction context cannot easily roll back the git state since it has already been committed and pushed manually.
2. **State Sync Overhead**: If `reflect` is executed inside the worktree, the local `frontier_state.*` files updated inside the worktree are not synced back to the main repository until the PR is merged and pulled.

To resolve these issues, we aim to make all git operations fully owned by the SPAO loop during `spao node reflect`.

---

## 1. Operator Decisions & Chosen Architecture

The operator aligned on **Option 3: Combined Approach**.

* **Invocation Boundary**: `spao node reflect` can be executed directly from the **main repository root** rather than requiring the agent to `cd` into the worktree.
* **Worktree Auto-Resolution**: The orchestrator will automatically resolve the active worktree path (e.g. from the active node's metadata in `frontier_state.yml`).
* **Auto-Staging**: By default, it will auto-stage all modified and untracked changes in the target worktree before committing.
* **Granular Staging Control**: It will support an optional `--stage` flag to filter specific files or to disable auto-staging.

---

## 2. Transaction Boundaries and Rollback Actions

When git operations are owned by the SPAO transaction context:
- **Local Staging Rollback**: If a commit fails, the transaction unstages the files (e.g., `git-reset`).
- **Commit Rollback**: If the push or PR creation fails, the transaction rolls back the local commit (e.g., `git-reset --hard HEAD~1` in the worktree).
- **Remote Push Rollback**: If PR creation fails after pushing, the remote branch can be deleted or force-pushed back to its base state.
