# Frontier Dyad — Practice Reflection — 2026-06-09 — System Crash Bug Fixes

## 1. CONTINUE — what worked
**Narrative (Operator):** 
**Details (Agent):**
- **Sluice Gate Triage Discipline:** The introduction of SG-0008 (Triage Holding) properly caught the `FRONTIER_INTEGRITY_VIOLATION` issues from polluting the execution loop further and successfully converted them into discrete bug nodes (Node 1931 and 1926) for tracking.
- **Autonomous Substrate Execution:** We fully verified that `sync` autonomously identifies, isolates, and initiates `plan-start` for bug nodes, allowing the system to pivot quickly to triage mode when faults are discovered.
- **Dormancy Invariants:** Proper maintenance of True Dormancy during HTIL waits and asynchronous test executions correctly prevented looping states and false assumptions.

## 2. START — what to do better
**Narrative (Operator):**
**Details (Agent):**
- **Test Sandbox Awareness:** Ensure `ANTIGRAVITY_RUNNING_TESTS=1` is consistently used when manually invoking `pytest` to prevent systemic tools (e.g., `daemon_telemetry.py`) from breaking due to unmocked side-effects.

## 3. STOP — what hurt (or almost did)
**Narrative (Operator):**
**Details (Agent):**
- **Mock Contamination in Telemetry:** Running `pytest` locally without the proper environment variables caused `daemon_telemetry.py` to evaluate mocked JSON output as a directory path (`get_workspace_dir()`), causing cascading `OSError: [Errno 22]` failures across multiple disconnected tests. 
- **Implicit Status State Leakage:** `bin/node abort <id>` released the active execution lock but did not reset the actual state status back to `Backlog` inside `frontier_state.yml`, causing `daemon_nba.py` to incorrectly raise `Mutually Exclusive Residence Violation` on subsequent iterations.

## Forward
The `FRONTIER_INTEGRITY_VIOLATION` bugs originating from decoupled caches and detached `HEAD` pushes have been fully remediated and tested. The system correctly synchronized and automatically dropped into Node 1920 (Harmonize - Path: Implement Two-Tier Backlog Abstraction). Node 1920 is now locked and ready for checkout.
