# Implementation Blueprint 1627: Plan - [BUG] Intake: System Crash in set-status

## Objective
Update `kernel/daemon_status.py` to gracefully handle invalid status keys instead of crashing, aligning with the philosophical immune boundary described in Discovery 1626.

## Target Changes
1. **File**: `kernel/daemon_status.py`
2. **Logic Update**:
   - In the section where the status key is processed, read the valid keys from `node.yml` (`node_attributes.status`).
   - Validate the incoming status argument against these valid keys.
   - If the key is invalid, print a descriptive error message outlining valid options and exit with `sys.exit(2)` (command line usage error) instead of raising an uncaught exception.

## Testing Strategy
1. **Unit Test**: Modify or add a test in `tests/test_daemon_status.py` to assert that providing an invalid status key results in a non-zero exit code and an informative error message, rather than a crash.
2. **Local Verification**: Run `./bin/node set-status <id> invalid_status` and verify the graceful error message.
