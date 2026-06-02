# Discovery 1626: Harmonize - [BUG] Intake: System Crash in set-status

## The Defect
When executing `./bin/node set-status <id> completed`, the system crashed with the following error:
`Status key 'completed' is not defined in node.yml`
This crash was intercepted by the wrapper/daemon, resulting in the creation of bug issue 1625.

## Root Cause Analysis
The `kernel/daemon_status.py` script attempts to look up the provided status key in `node.yml` (e.g., `completed`).
Since `completed` is not defined in the `node_attributes.status` mapping, the code throws an exception or fails an assertion without a graceful error message, causing the execution to crash rather than returning a controlled exit code with a validation error.

## The Philosophical Alignment
In the Dyad Wu-wei framework, operator commands (like `set-status`) represent intent. If the intent is malformed (e.g., passing an invalid status key), the system should act as an immune boundary, rejecting the malformed input gracefully and informing the operator of the valid options, rather than crashing.

## Proposed Remediation (Feedforward to Plan Phase)
1. **Validation Check**: Update `kernel/daemon_status.py` to validate the incoming status key against the keys present in `node.yml`.
2. **Graceful Exit**: If the key is invalid, print a descriptive error message indicating the valid keys and exit with a standard error code (e.g., `2` for usage error) instead of raising an uncaught exception.
