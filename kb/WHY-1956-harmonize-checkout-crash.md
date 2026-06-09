# WHY-1956: Harmonize [BUG] Intake: System Crash in checkout

## The Friction
Similar to the issue remediated in Node 1952, the Agent encounters a system crash when passing an invalid branch name during the `bin/node checkout` lifecycle phase. The underlying `TerminalNode.checkout()` method in `kernel/node_lifecycle.py` throws a standard `ValueError(f"Branch name MUST follow the standard: node/<id>-<kebab-case> or domain prefix")`.

Because it is a standard runtime exception, it triggers the telemetry decorator's global catch-all, logging an unhandled `System Crash` incident onto the backlog via the Intake daemon. This is a false positive and violates `WHY-1528: System Crash Validation Errors Rationale`.

## Dialectical Synthesis
A branch name validation failure during checkout is a predictable rejection of malformed Operator or Agent input. It is an intentional boundary guard, not a defect in the SPAOR loop's execution substrate. Therefore, it must not be logged as a crash.

## The Survivor (Harmonization)
Consistent with `WHY-1528` and the reflection in `WHY-1952`:
1. The intentional validation check for branch names in the `checkout` lifecycle block must gracefully halt using `sys.exit("[🚫 BLOCKED] Branch name MUST follow the standard: node/<id>-<kebab-case> or domain prefix")`.
2. This will ensure telemetry interprets the halt as a valid, intentional pipeline block rather than a structural engine failure.
