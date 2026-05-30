# WHY-1437: Prevent Empty PR Reflection Invariant

## 1. Intent
This document codifies the invariant that strictly blocks the reflection of a Node if there are no meaningful file changes (staged, unstaged, or committed) relative to the remote `origin/main`. 

## 2. Context & The Bug (Node 1422 Falsification)
Historically, the `reflect` lifecycle command included an "Administrative Node HITL Bypass" logic, which autonomously merged PRs if the PR ONLY modified files within `artifacts/` or `kb/`. 

The system's frontier editor natively modifies `artifacts/frontier_state.md` during the `reflect` process. If an Operator or Agent executed `reflect` on an Activity Node *without* having made any actual application/code modifications, the execution sequence would:
1. Modify `artifacts/frontier_state.md`
2. Automatically stage and commit the workspace
3. Create a PR containing *only* the `frontier_state.md` changes
4. Interpret the PR as a pure administrative change (since it only touched `artifacts/`) and **autonomously merge the empty PR**.

This caused the "Empty PR Bug" (Node 1422), violating the fundamental requirement that non-administrative Nodes must produce tangible state changes to be merged.

## 3. The Invariant
To mathematically falsify this failure mode, the `reflect` command now asserts a strict **Prevent Empty PR Guard** *before* the frontier state is mutated:

- **Condition**: The working tree MUST contain either uncommitted file modifications (`git status --porcelain` is non-empty) or the active branch MUST contain commits ahead of `origin/main` (`git diff origin/main` is non-empty).
- **Enforcement**: If both checks are empty, the reflection is forcefully aborted with an `Exception`. The system will refuse to mutate the frontier or generate an empty PR.

## 4. Administrative Parity
This guard perfectly distinguishes legitimate administrative bypasses from accidental empty PRs:
- If an Operator intends to reflect a purely administrative node, they must have explicitly modified a file (e.g., creating a new `WHY-*.md` document or manually updating the ledger). The guard will detect these modifications and allow reflection.
- If no files were modified, the reflection is blocked, enforcing true implementation intent.
