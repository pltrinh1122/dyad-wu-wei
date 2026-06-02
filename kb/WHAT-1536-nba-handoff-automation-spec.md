# WHAT: NBA Handoff Automation Spec

## Intent
Falsify the manual Operator handoff required to transition from zero WIP back into the Next-Best-Action (NBA) path. Automate the acquisition of the NBA lock via existing synchronous CLI entry points.

## Mechanism
- **Hook Locations:** `bin/status` and `bin/sync-clean` (or their respective Python daemons `kernel/daemon_status.py` and `kernel/daemon_node.py`).
- **Trigger Condition:** The workflow executes its normal logic (e.g. printing the status or syncing). At the very end, it checks if `Active Node : None` (i.e. WIP=0).
- **Execution:**
  1. The daemon evaluates the highest-scored NBA from the global backlog.
  2. If the NBA is valid and no active lock exists, the script automatically triggers an internal invocation equivalent to `./bin/node plan-start <NBA_ID>`.
  3. The Operator's terminal visually outputs the newly acquired lock, preserving observability without requiring an explicit manual input.

## Constraints
- **Race Condition Safety:** The automation MUST NOT execute in a detached background thread or cron job. It must be strictly bound to the final synchronous execution step of `bin/sync-clean` or `bin/status`.
- **Persona Context:** The automation must inherit the active `SPAO_PERSONA_ID` context. If the NBA is blocked by a persona gate, the automation simply prints the gate block and gracefully halts (yielding to the Operator).
