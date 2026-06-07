# WHY-1803: Checkout Crash Triage and Harmonization

## Problem Statement
The automated bug intake system reported a crash in the `checkout` subcommand:
`ValueError: Branch name MUST follow the standard: node/<id>-<kebab-case>`

This crash occurred because the `cmd_checkout` function allowed the `ValueError` raised by invalid branch naming conventions to bubble up as an unhandled exception. This unhandled exception then triggered the system's automated bug intake logic, creating a backlog issue and disrupting flow state with an Iatrogenic (system-caused) feedback loop.

## Philosophical Alignment
The Wu-wei SPAOR engine operates under the principle of Gateless Autonomous Execution. However, when user input or systemic formatting is invalid, the engine must distinguish between a genuine system crash (e.g., an API failure or unhandled null pointer) and a validation failure (e.g., malformed branch name, invalid node ID).

Validation failures are NOT system crashes; they are expected boundaries. Allowing a validation boundary to trigger an automated bug intake violates the autonomy principle by conflating human error with systemic fragility.

## Technical Intent
To resolve this, we must adopt the same pattern implemented for `set-status` in Node 1658:
1. `cmd_checkout` in `daemon_node.py` must be wrapped in a `try...except ValueError` block.
2. When a `ValueError` is caught, the system MUST gracefully terminate execution using `sys.exit(2)` rather than raising an unhandled exception.
3. This prevents the top-level exception handler from interpreting the validation failure as a systemic crash, thus stopping the autonomous bug-reporting loop.

## Execution Directives
- **Plan Phase (Node #1804)**: Design the try-except wrapper around `checkout_node` in `daemon_node.py`.
- **Reflect Phase (Node #1805)**: Implement the change and ensure the test suite is updated to assert that `sys.exit(2)` is invoked on invalid branch names.
