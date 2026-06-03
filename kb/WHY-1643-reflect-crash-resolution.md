# WHY-1643: Reflect Crash Resolution

## Abstract
This document formalizes the harmonization resolution for the `FileNotFoundError` crash encountered during the `reflect` lifecycle phase ([Path 1642]).

## Root Cause Analysis
The crash was traced to an obscure `FileNotFoundError` originating from `subprocess.Popen` when `git_client.status_porcelain(cwd=worktree_dir)` is executed inside `kernel/node_lifecycle.py::reflect()`. 

This condition occurs exclusively when an Agent violates the SPAO execution invariant by invoking the `./bin/node reflect` command from *inside* an active worktree directory (e.g., `cd .worktrees/node/XXX` then `./bin/node reflect`). When invoked from within the worktree, `path_resolver.get_core_dir()` incorrectly resolves the worktree root as the core repository root. Consequently, `get_worktree_path()` appends the `.worktrees/...` path a second time, resulting in a double-nested directory path (e.g., `.worktrees/node/XXX/.worktrees/node/XXX`) that does not exist, triggering the fatal crash.

Because the crash presents as an unhandled `FileNotFoundError`, the telemetry daemon intercepts it and autonomously files a bug report, masking the underlying invariant violation and seizing the Agent's execution loop.

## Harmonized Resolution Strategy
To resolve this defect, the system must transform the unhandled traceback into a graceful, structural gate enforcement. 

**Implementation Directives (Node 1644 / 1645):**
1. Implement a safety guard at the beginning of the `reflect` command sequence.
2. The guard must explicitly verify that `get_core_dir()` and the current execution context point to the true repository root, not a `.worktrees` directory.
3. If an invalid execution context is detected, the system must immediately raise a controlled exception: `sys.exit("[🚫 BLOCKED] Reflection Blocked: You must run the reflect command exclusively from the repository root directory, not from within the active worktree.")`

This approach ensures the system enforces the operational invariant transparently, allowing the Agent to self-correct its `Cwd` without triggering anomalous bug reports or catastrophic seizures.
