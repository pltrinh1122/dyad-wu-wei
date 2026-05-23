# Retrospective: Node 803 Reflection Rollback

## The Violation
During the reflection phase of Node 803, the GitHub CLI command `gh pr list` encountered a transient network/API failure (returning exit status 1). This failure triggered the FlowTransaction rollback, reverting the issue closure and frontier updates, and logging a failure event in the telemetry.

## The Root Cause
1. **GitHub API Dependency**: `create_pull_request` executes `gh pr list` to check for existing pull requests for the head branch.
2. **Transient Error**: A transient API connection failure or rate limit block on GitHub's side caused the CLI command to fail.
3. **Purity Invariant Trigger**: The telemetry recorded this failure event, which activated the mandatory post-failure reflection check on subsequent reflection attempts.

## The Epistemic Insight
Telemetry records all command failures (including transient external network errors) as failures. These must be explicitly acknowledged and resolved. When a transaction rollback occurs, we must prune remote branches, reset local worktrees, and document the event before re-reflecting.

## The Remediation
1. Delete the remote branch on GitHub to prevent fast-forward conflicts.
2. Reset the local worktree branch to origin/main.
3. Document the failure in this retrospective file (`artifacts/audit/retro-803.md`) to satisfy the post-failure reflection gate.
4. Re-execute the reflection command.
