# WHY-2221: Harmonize [BUG] Intake: System Crash in sync

## The Friction
During the `bin/node sync` lifecycle phase, if the `artifacts/frontier_state.yml` has been manually modified by the Operator or corrupted, the `kernel.agent_frontier.load_state` method correctly raises a `StateCorruptionError` because the checksum does not match its `.sha256` counterpart.

However, because this is a standard custom runtime exception that is not caught by the `cmd_sync` handler in `kernel/daemon_node.py`, it propagates up and triggers the telemetry decorator's global catch-all. This results in logging an unhandled `System Crash` incident onto the backlog via the Intake daemon. This is a false positive and violates the CSI Governance HTIL principles outlined in `WHY-1528: System Crash Validation Errors Rationale`.

## Dialectical Synthesis
A checksum mismatch is a known, predictable state that alerts the Operator to out-of-band edits and provides instructions to run `./bin/meta rehash`. It is an intentional boundary guard to prevent state corruption propagation, not a defect in the SPAOR loop's execution substrate. Therefore, it must not be logged as an unhandled system crash.

## The Survivor (Harmonization)
Consistent with `WHY-1528` and the reflection in `WHY-1956`:
1. The intentional validation check for the frontier state checksum must gracefully halt using `sys.exit(f"[🚫 BLOCKED] {e}")` when catching `agent_frontier.StateCorruptionError` inside `daemon_node.py` (specifically `cmd_sync` or `sync_and_clean_node`).
2. This will ensure telemetry interprets the halt as a valid, intentional pipeline block requiring Operator intervention, rather than a structural engine failure.
