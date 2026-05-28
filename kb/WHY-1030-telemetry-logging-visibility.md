# WHY-1030: Telemetry Logging Visibility and Unbuffered Standard Output

## Classification
- **Type**: WHY (Architectural Decision Record)
- **ID**: WHY-1030
- **Author**: agent-sg5 (SG-0005: Autonomous Knowledge Accrual)
- **Created**: 2026-05-28 (Node 1030, Path 1029)
- **Context**: Explaining the telemetry output buffering issue during background task execution and the unbuffered stdout/flush fix.

---

## 1. The Telemetry Visibility Problem

When executing multi-step agentic operations in the background (such as the SPAO loop transitions run inside subagents or background terminals), log outputs were previously buffered. This occurred because Python's default standard output buffering behavior for non-interactive streams (e.g. when stdout is redirected to a log file or piped) delays writing to the disk/pipe until the buffer is full or the process exits.

Consequently, the Operator and automated audit sensors were "blinded" to real-time execution states:
- Stage advancement logs (e.g., `log_stage_advancement` in `node_lifecycle.py`) were not immediately visible in background task logs.
- Automated gates checking logs for completion indicators would stall, wait indefinitely, or assume the process had crashed.

---

## 2. Technical Implementation details

To resolve stdout buffering without introducing unnecessary print wrappers, `log_stage_advancement` has been updated to force unbuffered output emission.

### 2.1 Direct Flush Protocol
Every telemetry stage transition event written to `sys.stdout` must be immediately flushed to guarantee visibility:
- **`sys.stdout.write(message)`**: Write raw output directly to standard output.
- **`sys.stdout.flush()`**: Force the OS to flush stdout's internal buffer to the file descriptor immediately.

### 2.2 Systemd and Subprocess Compatibility
By flushing stdout immediately, log streams captured via background tasks (using `manage_task` logging, `run_command` output capture, or `systemd --user` journal logs) receive real-time telemetry events synchronously with the actual code execution, preventing downstream timeouts or eventual consistency sync lag.

---

## 3. Invariants and Guardrails

1. **Stdout Purity**: Standard library `sys.stdout` writes are preferred for core lifecycle logging to ensure compatibility across virtual environments and terminal wrappers.
2. **Deterministic Telemetry Logging**: Telemetry transitions MUST NOT be suppressed or buffered. Any output related to the status or transition of SPAO phases must be flushed instantly.
