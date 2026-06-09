# WHY-1952: Harmonize [BUG] Intake: System Crash in reflect

## The Friction
During routine autonomous path execution, if the Agent passes an invalid branch name to `bin/node reflect`, the underlying function in `kernel/node_lifecycle.py` raises a `ValueError("Branch name MUST follow the standard: node/<id>-<kebab-case>")`. 

Because this is a standard Python runtime exception, it bubbles up to the global execution scope and is caught by `telemetry_decorator` as an unhandled system exception. This triggers an autonomous bug report `[BUG] Intake: System Crash in reflect`.

This violates the principle established in `WHY-1528: System Crash Validation Errors Rationale`, which dictates that intentional policy enforcement mechanisms (validation blocks) must be structurally distinct from unhandled system failures.

## Dialectical Synthesis
A branch name validation failure is an intentional rejection of a malformed state, not a defect in the runtime engine itself. It should not be logged as a System Crash or pollute the backlog with incident nodes.

## The Survivor (Harmonization)
To achieve alignment with `WHY-1528`:
1. The intentional validation check for branch names in `kernel/node_lifecycle.py` must halt execution gracefully using `sys.exit("[🚫 BLOCKED] Branch name MUST follow the standard: node/<id>-<kebab-case>")` rather than throwing a `ValueError`.
2. This ensures the telemetry decorator registers the exit as a controlled halt (exit code > 0) rather than an unhandled system crash, thereby suppressing false-positive bug intake generation.
