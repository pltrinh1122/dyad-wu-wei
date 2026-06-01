# WHY-1528: System Crash Validation Errors Rationale

## Core Principle
Intentional policy enforcement mechanisms (validation blocks) must be structurally distinct from unhandled system failures.

## Problem Context
When the SPAO execution loop intercepts an invalid state (e.g., attempting to `plan-start` a Path issue directly, or violating the `WIP-N=1` invariant), the orchestrator correctly blocks the execution. However, because these blocks were implemented using standard Python `raise Exception(...)` or `raise ValueError(...)`, they were indistinguishable from genuine runtime failures to the global `try/except` block in `daemon_node.py`.

This architectural conflation caused the `[❌ CRASH]` interception handler to erroneously file bug reports for routine validation rejections. This flooded the backlog with false-positive `[BUG] Intake: System Crash` nodes.

## Architectural Resolution
To preserve the fidelity of autonomous bug reporting, we formally delineate execution failures into two ontological categories:
1. **Validation Rejections (Intentional):** Handled via `sys.exit("[🚫 BLOCKED] ...")`. This gracefully halts the execution pipeline and signals the operator (or daemon) of the policy violation, without triggering an intake report.
2. **System Crashes (Unhandled):** Handled via the global exception handler, catching genuine defects (e.g., `AttributeError`, `IndexError`) and filing autonomous bug reports.

This guarantees that the autonomous backlog is only populated with genuine defects requiring Path generation.
