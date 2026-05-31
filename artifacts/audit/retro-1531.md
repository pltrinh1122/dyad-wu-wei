# Post-Mortem: Node 1531 (System Crash in sync)

## Incident Summary
A system crash occurred during the `sync` stage due to a bug in `TelemetryDaemon.record_event`. The correct method was `log_event`. 
This caused an intake crash which triggered an execution failure.

## Root Cause
`record_event` was incorrectly called on `TelemetryDaemon` instead of `log_event`.

## Resolution
Replaced `telemetry.record_event` with `telemetry.log_event(stage="SYSTEM", event="ERROR", metadata={...})` in `kernel/daemon_node.py`.
