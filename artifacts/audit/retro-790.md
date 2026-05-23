# Post-Mortem: Node 790

## The Failure
The node reflect command failed with a `FileNotFoundError` due to executing `reflect` from within the active worktree (`.worktrees/node/790-probe-align-cron-job-portability`). The `daemon_node.py` script computes the worktree path assuming execution from the repository root. When executed from within the worktree, the relative paths concatenate incorrectly, causing a crash.

## The Codified Insight (WHY/HOW)
**HOW-0001 SPAO Execution Loop Update:**
All `bin/node` commands, specifically `checkout` and `reflect`, must be executed from the absolute root of the main repository, NOT from within the `.worktrees/` directory, to ensure relative path resolution for git operations succeeds.
