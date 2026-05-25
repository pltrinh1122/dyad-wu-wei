# Retrospective 1007: FlowTransaction Failure During HTIL Bypass

## Context
During the reflection of Node 1007 (an administrative node), the system correctly bypassed the HTIL manual merge gate and successfully merged the PR via `gh pr merge`.

## The Failure
The orchestrator encountered a `CalledProcessError` on `gh pr merge --squash --delete-branch`. The failure was due to two compounding factors:
1. The new `merge_pull_request` function in `github_client.py` suffered a namespace collision with an identical legacy function taking `(pr_number: int)`. Python overwrote the new function with the old one, causing `node_lifecycle.py` to accidentally call the legacy command which implicitly injected the `--delete-branch` flag.
2. Because the agent was still checked out in `node/1007-hygiene-audit`, Git rejected the `--delete-branch` attempt, crashing the script and triggering an automatic transaction rollback.

## The Codified Insight (WHY)
The newly introduced HTIL-bypass merge function has been explicitly renamed to `admin_merge_pull_request(pr_url: str)` to avoid namespace collisions. The `gh pr merge` operation natively handles URL-based merging without requiring `--delete-branch`, allowing the local orchestrator to cleanly manage its own worktree teardown.
