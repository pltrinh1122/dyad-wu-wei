# Node 713 Retrospective

## Execution Failure
During the execution of Node 713 (Align), an execution failure occurred: `FileNotFoundError` was raised because `bin/node reflect` was executed from inside the `.worktrees/node/713-align-dz-cil` directory, which appended the worktree path recursively. Another failure occurred during checkout due to a `subprocess.CalledProcessError` on `gh issue edit` returning exit code 1.

## Root Cause
1. `gh issue edit` returned exit code 1 because the GraphQL API deprecation warning printed to stderr triggered `check=True` in `subprocess.run()`, despite the command actually successfully adding the label.
2. `bin/node reflect` expects to be run from the repository root, as `node_lifecycle.py` calculates worktree paths relative to the current working directory.

## Remediation / Invariants Added
- Run all `bin/` scripts from the repository root, NOT from inside the worktrees.
- Removed `check=True` from `github_client.py` where CLI commands print expected stderr deprecation warnings, or ensure `stderr` is not conflated with fatal errors.

## Path Forward
The Align node successfully generated the DZ-CIL Manifesto (`kb/WHAT-0000-dz-cil-manifesto.md`) as planned, maintaining architectural direction.
