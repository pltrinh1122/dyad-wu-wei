# Retrospective 1010: Improper Git Reset

## Context
During the rollback recovery for Node 1010, the HTIL Bypass script crashed for the third time with the exact same namespace collision error on `--delete-branch`.

## The Failure
The previous rollback script executed `git reset --soft origin/main`. A soft reset only moves HEAD but preserves the working tree and index exactly as they were. Therefore, `node_lifecycle.py` in the worktree was never actually updated to the version from `origin/main` that contained the PR 1009 fix.

## The Codified Insight (WHY)
When executing a Rollback Protocol to absorb upstream bug fixes, the Agent MUST use `git reset --hard origin/main` to forcefully synchronize the working tree. This ensures the execution environment is identical to the remote tip. The recovery has been executed with a hard reset, permanently resolving the collision.
