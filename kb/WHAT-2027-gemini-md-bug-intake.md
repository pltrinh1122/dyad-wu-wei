# WHAT-2027: Technical Implementation for "GEMINI.md changed" Intake

## 1. Goal
Halt the system without polluting the backlog when `GEMINI.md` or `AGENT.md` is changed, and properly route `dispatch_alert` tags based on semantic severity.

## 2. Requirements

1. **Refactor `dispatch_alert` (in `drivers/audit_daemon.py`)**:
   - Extract the alert severity from the message prefix (e.g., `[FAILURE]`, `[NOTIFICATION]`).
   - If the severity is `[FAILURE]`, use `[ALERT] Intake:` as the prefix.
   - If the severity is `[NOTIFICATION]`, use `[NOTICE] Intake:` as the prefix.
   - Fallback to `[BUG] Intake:` only if no semantic tag is found.
   
2. **Refactor `file_modified` rules (in `infra/audit-daemon/audit_config.yml` and `drivers/audit_daemon.py`)**:
   - For `agent-md-changed` and `gemini-md-changed`, change `alert_level` to a new custom level: `HALT_NO_INTAKE` or similar, OR add a `create_intake: false` flag.
   - Update `evaluate_file_modified` in `audit_daemon.py` to check for `create_intake: false`. If true, print the message to `stdout` to hard-halt the agent via the terminal hook, but skip calling `dispatch_alert()`.

3. **Purge Orphaned Node**:
   - Close the existing `[BUG] Intake: GEMINI.md changed` backlog path, as it is obsolete.

## 3. Implementation Plan
This will be executed in the subsequent Act phase of Path 2027.
- Checkout Act Phase Worktree.
- Modify `audit_daemon.py`.
- Modify `audit_config.yml`.
- Run tests (`bin/run-tests`).
- Run `bin/node reflect`.
