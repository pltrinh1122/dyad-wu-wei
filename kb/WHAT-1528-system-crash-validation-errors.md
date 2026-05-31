# WHAT-1528: System Crash Validation Errors Architecture

## Context
The SPAO system utilizes a unified exception catching mechanism in `daemon_node.py` to intercept unhandled exceptions and autonomously file bug reports (Intake Issues). However, various intentional validation gates (e.g., WIP-N=1, Quarantine Gate, Persona Gate, and Harmonization checks) were implemented by throwing generic `Exception` or `ValueError`.

When a user or daemon triggers one of these validation gates (such as attempting to `plan-start` a Path issue directly, or violating WIP-N=1), the validation exception is caught by the global error handler, resulting in a false-positive system crash report. This causes recursive intakes like "[BUG] Intake: System Crash in plan-start".

## Design Decision
Validation blocks are intentional mechanism rejections, not unexpected system failures. They must not trigger autonomous bug reporting.

1. **Clean Exit for Validation:** All intentional validation rejections MUST utilize `sys.exit(f"[🚫 BLOCKED] {message}")` instead of raising exceptions.
2. **Global Error Handler Preservation:** The global exception handler in `daemon_node.py` remains in place to catch genuine unhandled exceptions (e.g., `AttributeError`, `TypeError`, network failures) to ensure true crashes are reported.
3. **ValidationError Class:** A specific `ValidationError` class is defined in `daemon_node.py` to allow the CLI to gracefully block execution without triggering the bug reporter, should internal CLI logic require exception-based control flow prior to `sys.exit`.

## Implementation Strategy
- Replace all instances of `raise Exception(...)` with `sys.exit("[🚫 BLOCKED] ...")` within `kernel/node_lifecycle.py` for all validation gates (Orthogonal Scope, Quarantine, WIP-N=1, Reflection Blocked).
- Replace all instances of `raise Exception(...)` and `raise ValueError(...)` with `sys.exit("[🚫 BLOCKED] ...")` within `kernel/daemon_strategic.py` for Persona Gate and Harmonization checks.
- Add `ValidationError` to `daemon_node.py` to handle any CLI-specific validation routing.
