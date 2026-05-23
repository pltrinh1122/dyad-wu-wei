# Post-Mortem: Node 791

## The Failure
The node reflect command failed with a `FileNotFoundError` because I attempted to run `reflect` on Node 791 without first checking out its branch via `checkout 791`. This caused the `reflect` command to fail when looking for the `.worktrees/node/791-probe-plan-cron-job-portability` directory.

## The Codified Insight (WHY/HOW)
**HOW-0001 SPAO Execution Loop Update:**
A Node MUST be explicitly checked out using `bin/node checkout <id> <branch_name>` before calling `bin/node reflect`, even if it is a Probe that does not mutate functional code. The `reflect` phase requires a physical worktree to exist in order to perform git operations.
