# WHAT: Resolve System Crash in `plan-start` (Issue #2069)

## Context
A system crash was encountered in the `plan-start` subroutine during execution of a node. The crash report identified that a `StateDissonanceError` triggered a fallback system bug report rather than being gracefully caught and logged as `[🚫 BLOCKED]`. Additionally, a "SPEC file violation" blocked the node completion because the `plan-start` command matched the `"plan" in title.lower()` check, improperly classifying implementation nodes as `Plan` nodes.

## Intended Behavior
1. The `daemon_node.py` CLI boundary must natively catch and handle `StateDissonanceError` (and other intentional blocking exceptions like `StateCorruptionError`) cleanly without bubbling up to the fallback telemetry crash reporter.
2. The `node_lifecycle.py` check for SPEC files must accurately target `Plan` nodes by using strict regex boundaries (`r"^(?:(?:Node|Path|Discovery|Activity)\s*\d+:\s*|#\d+:\s*)?Plan\b"`) rather than broad substring matches.

## Implementation (Already merged in PR #2074)
- `kernel/daemon_node.py`: Wrapped `cmd_plan_start`, `cmd_checkout`, `cmd_sync`, etc., or the main dispatcher, to cleanly catch the intended guard exceptions.
- `kernel/node_lifecycle.py`: Updated `_verify_state_purity` and the `Plan` phase regex validation to avoid false positives.
