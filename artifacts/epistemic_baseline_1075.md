# Epistemic Baseline: Agentic Bug Reporting (Node 1075)

## 1. Current State of Exception Handling
- `kernel/daemon_node.py` main execution block (`if __name__ == "__main__": main()`) does not currently wrap commands in a global `try/except` block. Exceptions raised during Node operations (`plan`, `checkout`, `reflect`) bubble up directly to `stderr`, crashing the execution script.
- `kernel/daemon_telemetry.py` logs explicit `START` and `FINISH` events but does not natively catch or log `ERROR` or `CRASH` events on unhandled exceptions.

## 2. Current State of Backlog Integration
- `kernel/daemon_backlog.py` handles creating issues. It currently supports paths and nodes. It relies on GitHub API interactions (`drivers/github_client.py`).
- There is a `Triage Holding` path (Path 1242) and a `status:triage` label used for bugs and external intakes (as seen in open issues).

## 3. Mechanisms for Agentic Bug Interception
To build a resilient bug reporting mechanism, we must:
1. **Global Exception Interceptor**: Implement a global `try/except Exception as e` wrapper around CLI entry points.
2. **Traceback Capture**: Extract the full stack trace (`traceback.format_exc()`), the execution context (Node ID, SPAO Phase, active worktree), and standard environment details.
3. **Automated Issue Generation**: Within the global exception handler, call a specialized method in `daemon_backlog.py` (e.g., `report_system_bug(traceback, context)`) that creates an issue with:
   - Prefix: `[BUG] ` or `Intake: System Crash`
   - Label: `status:triage` and `bug`
   - Body: Formatted markdown containing the captured telemetry context.
4. **Telemetry Logging**: Enhance `daemon_telemetry.py` to record an `ERROR` event alongside standard telemetry when a crash occurs.
5. **Graceful Exit**: Output a clear warning to the Agent/Operator with the URL of the newly created bug report, so the Agent can pivot or wait for resolution without becoming stuck in an invisible error loop.
