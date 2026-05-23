# Retrospective 805: Merge Conflict Prevention Bypass

## Incident Description
During the execution of Node 805, the `reflect` command completed locally without detecting any merge conflicts, but the resulting Pull Request triggered a merge conflict on GitHub (preventing merge and forcing operator intervention).

## Violation
The invariant established in **WHY-0083** (The Agent is responsible for resolving its own merge conflicts) was violated because the agent relied on a stale local representation of the `origin/main` tracking branch.

## Root Cause Analysis
1. The `check_merge_conflicts("origin/main")` safeguard evaluates the git tree against the locally cached tracking branch.
2. The `reflect` daemon in `kernel/node_lifecycle.py` did not invoke a network fetch prior to executing this check.
3. Thus, if `origin/main` advanced asynchronously during execution, the safeguard falsely reported a conflict-free state, allowing the PR to be pushed with embedded remote conflicts.

## Resolution & Insight
- **Insight (WHY-0085)**: All Git state evaluations (conflict checks, branching, checkout) MUST explicitly synchronize with the remote (`git fetch origin`) prior to execution to prevent stale state hallucinations.
- **Materialization**: `kernel/node_lifecycle.py` was updated so that both `checkout` and `reflect` invoke `git_client.fetch("origin")` before interacting with the remote state. `git_client.worktree_add` was also updated to explicitly branch off `origin/main` rather than `main`.
