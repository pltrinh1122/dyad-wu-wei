# Retrospective 1010: Stale Node Sync Crash

## Context
During the reflection of Node 1010, the HTIL Bypass script successfully autonomously merged the PR, but the script then crashed on `gh pr merge --delete-branch`.

## The Failure
The local `main` was stale. Despite `node sync` being executed earlier, the sync failed to incorporate PR #1009 (which contained the fix for the HTIL bypass namespace collision) due to an intervening `CRITICAL ROM DRIFT` restart sequence. Consequently, the local orchestrator executed the outdated version of `node_lifecycle.py`, tripping the exact same `--delete-branch` error as Node 1007.

## The Codified Insight (WHY)
The rollback protocol has been applied to cleanly reset the worktree to the remote tip, explicitly pulling down the previously merged PR 1009 fix to permanently resolve the namespace collision.
