# WHAT-1076: Agentic Bug Reporting Specification

## Classification
- **Type**: WHAT (Technical Specification)
- **ID**: WHAT-1076
- **Author**: agent-sg5
- **Created**: 2026-05-30 (Node 1076, Path 1074)
- **Related Path**: Path 1074 (Establish robust agentic bug reporting and triage mechanisms)

---

### 1. Scope & Goals
To ensure the Metasystem is resilient against unhandled exceptions during execution, we must build an autonomous agentic bug detection and reporting mechanism. This system will allow the Agent to dynamically intercept crash traces, file formal issues into the Triage Holding backlog, and alert the Operator, avoiding execution lockups.

---

### 2. Global Exception Interceptor Rules
1. **Entry Point Wrapping**:
   - The primary entry point for all node daemons (`kernel/daemon_node.py` main block) MUST wrap command executions in a global `try/except Exception as e:` block.
2. **Context Preservation**:
   - The exception handler must extract `traceback.format_exc()`, the current execution phase, and the active `SPAO_PERSONA_ID`.
3. **Automated Issue Generation**:
   - The exception handler MUST invoke `daemon_backlog.py` to create a new GitHub Issue.
   - The issue title MUST be prefixed with `[BUG] Intake: System Crash in {subcommand}`.
   - The issue MUST be tagged with the `status:triage` label and the `bug` label.
   - The issue body MUST include the captured traceback and context, formatted cleanly in a markdown code block.
4. **Telemetry Logging**:
   - The exception handler MUST invoke `daemon_telemetry.py` to record an `ERROR` event.

---

### 3. Graceful Pivot & Recovery
Instead of allowing the script to terminate with a generic Python traceback on stderr, the script MUST output a clear, user-facing error message to the terminal stating that a system crash was intercepted, and it MUST provide the URL of the newly created GitHub bug report. This guarantees the Agent can ingest the failure state gracefully and pivot to resolving the bug or informing the Operator.
