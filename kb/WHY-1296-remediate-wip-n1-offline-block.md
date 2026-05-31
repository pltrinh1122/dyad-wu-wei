# WHY-1296: Remediate sync_and_clean_node WIP-N=1 offline block

## Context
Path 1296 sought to auto-fetch closed/merged PR status from GitHub before raising an offline WIP-N=1 violation for local worktrees. This prevents manual blocks when the system runs in an offline-by-default local sync but an active worktree's PR has already been merged remotely.

## Falsification / Harmonization
Upon investigation in Node 1297, it was discovered that this mechanism was already autonomously implemented by the Operator in commit `1c1e2a2a` (on 2026-05-28) in `kernel/daemon_node.py`. The `sync_and_clean_node` implementation (and `clean_if_merged`) correctly queries the `get_pr_state_by_branch` GitHub API and cleans the worktree before considering it an open WIP violation.

## Conclusion
No further code changes are required for Path 1296. This Path acts as a formalization and administrative closure of the intent. The logic gate is proven to be correctly positioned in `kernel/daemon_node.py`.
