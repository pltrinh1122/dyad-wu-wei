# Retrospective: Node 2221

## 1. Description of the Error
During the execution of `./bin/node reflect 2221`, the system crashed with the following error:
```
Exception: Reflection Blocked (WHY-0083): Branch has unresolved merge conflicts with 'origin/main'. Auto-resolution could not handle: ['artifacts/frontier_state.yml']. You must resolve these conflicts locally before reflecting.
```
This failure triggered a telemetry crash report (Issue #2168) and a rollback of the git transaction.

## 2. Root Cause Analysis
The `reflect` command in `kernel/node_lifecycle.py` attempts to automatically rebase the active node branch on top of `origin/main`. Because `frontier_state.yml` is automatically updated by the `reflect` script prior to rebasing, and `origin/main` had advanced and altered the same metadata block, the automatic Git merge resolution failed. This conflict could not be automatically reconciled, leading to an unhandled exception that broke the SPAOR loop execution substrate and invoked the global telemetry catch-all.

## 3. The Resolution
The branch was automatically rolled back. To safely resume, the Operator/Agent must:
1. Fetch and rebase the worktree directly onto `origin/main` before running the `reflect` phase.
2. Re-apply the `WHY-2221-harmonize-sync-crash.md` harmonization document over the latest `origin/main` tree.
3. Re-run `./bin/node reflect 2221`.

## 4. Feedforward Invariant
To prevent this issue in the future, the Agent must ensure that it pulls the latest `origin/main` before generating modifications that might touch highly contested files, or ensure the test validations naturally capture rebase conflicts proactively before hitting the `reflect` step.
