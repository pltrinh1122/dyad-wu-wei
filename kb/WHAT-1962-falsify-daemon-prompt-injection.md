# WHAT-1962: Falsify Daemon Prompt Injection

## Architecture
This document implements the structural remediation defined in `WHY-1960`. It enforces the **Intake Context Boundary Invariant**, ensuring that autonomous daemon processes do not conflate execution metrics with the conversational operator `prompt:` queue.

## Structural Changes (Already Compliant / Verified)
1. **Daemon DAG Mutation**: The `drivers/audit_daemon.py`'s `dispatch_alert` function translates alerts directly into `[BUG] Intake` issues on the DAG via the `BacklogDaemon`, structurally bypassing the `artifacts/prompt_backlog.yml` queue entirely.
2. **Sluice Gate Sensor**: The sensor detects `PR Merged` events and triggers `bin/node sync --remote` synchronously instead of injecting `[NOTIFICATION]` prompts.
3. **Queue Ownership**: The `prompt:` queue is strictly reserved for human Operator conversational intent.

## Execution Plan
- No further functional code changes are required, as the engine currently correctly routes background daemon alerts to the DAG as `[BUG]` nodes and executes silent operations.
- This plan ratifies the codebase's adherence to the `WHY-1960` invariant.
