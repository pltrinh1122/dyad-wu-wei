# Retro 776: Sluice Gate Sensor Execution Failures

## Incident
During the execution of Node 776, an execution failure was logged because the `node reflect` script was initially invoked from inside the `.worktrees/node/776-sluice-gate-sensor` directory instead of the `REPO_ROOT`, causing an `Errno 2: No such file or directory` when attempting to access `.worktrees` relative to itself.
Additionally, there was an initial failure attempting to run `python skills/audit_daemon.py` directly without activating the virtual environment.

## Root Cause
- The agent failed to switch back to the `REPO_ROOT` directory before running `./bin/node reflect`.
- The agent executed python directly without using `.venv/bin/python` or `./bin/run-tests` which automatically manages the environment.

## Codified Insight
1. Always run `./bin/node` orchestration commands from the repository root, not from inside the `.worktrees/` directories.
2. Always use `./bin/run-tests` or `.venv/bin/python` when executing python modules locally.
