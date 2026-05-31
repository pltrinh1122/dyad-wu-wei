# WHAT-1461: Stepped-Away Discipline Implementation Specification

## Classification
- **Type**: WHAT (Technical Specification)
- **ID**: WHAT-1461
- **Author**: agent-sg5
- **Created**: 2026-05-30 (Node 1461, Path 1459)

---

### 1. Scope & Goals
To implement the philosophic intent defined in `WHY-1460` (conserve compute and true dormancy during Operator absence), we must codify the technical execution steps for the Agent. This implementation will instruct the Agent to autonomously manage its own background heartbeat daemons during HTIL wait states.

### 2. Implementation Rules

1. **GEMINI.md (Agent Anchor) Update**:
   We will update the `Antigravity-Specific: Asynchronous Execution` section in `GEMINI.md` to include explicit instructions for the Stepped-Away Discipline:
   - When the Agent arrives at an HTIL block (e.g., after executing `reflect`) and prepares to yield its turn, it MUST explicitly use the `manage_task(Action="kill")` tool to terminate the recurring `audit_daemon.py` schedule.
   - When the Agent is awakened by the Operator's explicit prompt input (the Step-Back Discipline), it MUST use the `schedule` tool to immediately re-instantiate the `audit_daemon.py` background cron job before or during the Sense phase.

2. **Dormancy Execution**:
   - The Agent must not rely on `daemon_node.py` or other external scripts to kill its timers. It must proactively execute the `manage_task` tool call itself as part of its operational loop.

### 3. Execution Phase (Act)
In the subsequent Act phase, we will apply these modifications directly to `GEMINI.md` and ensure the prompt instructions cleanly guide the Agent to execute this behavior without ambiguity.
