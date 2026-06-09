# WHAT-1953: Plan - [BUG] Intake: System Crash in reflect

## Goal
Implement the technical resolution for the branch validation system crash identified in `WHY-1952`. The implementation must ensure that invalid branch names provided to `bin/node reflect` trigger a graceful `sys.exit` with a `[🚫 BLOCKED]` marker, preventing the `telemetry_decorator` from classifying it as an unhandled system crash.

## Architecture
1. **Target File**: `kernel/node_lifecycle.py`
2. **Target Method**: `TerminalNode.reflect()` (Line 530)
3. **Change**: Replace the current `raise ValueError("Branch name MUST follow the standard: node/<id>-<kebab-case>")` with a graceful termination that uses `sys.exit("[🚫 BLOCKED] Branch name MUST follow the standard: node/<id>-<kebab-case>")`.
4. **Validation**: The test suite must pass, confirming that the runtime logic remains intact while appropriately halting on invalid inputs.

## Success Criteria
- If `bin/node reflect` is called with an invalid branch name, it prints `[🚫 BLOCKED] ...` and exits with code 1 without printing a Python traceback.
- The `audit_daemon.py` and telemetry interceptors no longer map this event to a System Crash bug in the backlog.
