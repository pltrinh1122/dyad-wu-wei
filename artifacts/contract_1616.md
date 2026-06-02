# Activity 1616: Automate test gates in Node Reflect (Node Contract)

## Context & Rationale
The recent CI failures on PR #1611 and #1601 revealed a structural gap: the Agent was able to successfully create a PR using `spao node reflect` and `spao rt hotfix` even when local tests had not been run or were failing. To formally implement PR Discipline, we must codify this invariant by implementing automated test execution as a hard gate within these deployment drivers.

## Proposed Changes
- Modify `kernel/daemon_node.py` (specifically the `reflect` command) to execute `./bin/run-tests` synchronously.
- Modify `kernel/daemon_rt.py` (specifically the `hotfix` command) to execute `./bin/run-tests` synchronously.
- If the test suite fails, the deployment script MUST abort and refuse to push or create the PR.

## Pre-Requisite Invariants
- The worktree must contain the `bin/run-tests` script.

## Post-Requisite Invariants
- All tests pass before a PR is opened.

## Verification Plan
- Run tests via `spao test`.
- We will not intentionally fail a test in the live PR to test this, as it would require pushing broken code, but the code logic itself will be reviewed.

## User Review Required
> [!IMPORTANT]
> Please review the test gate implementation in daemon_node.py and daemon_rt.py.
