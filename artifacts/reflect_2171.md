# Reflect - Node 2171: Final Reflection for System Crash in reflect

## Retrospective
**What went wrong:**
During the execution of a `reflect` command, if a local invariant (like `enforce_reflection_hook`) failed or a file was missing, it surfaced as an unhandled exception (e.g., `FileNotFoundError`), causing the entire daemon process to crash and forcing a bug intake loop.

**What was done:**
Node #2182 caught `ReflectionBlockedError` directly within `kernel/node_lifecycle.py`. This ensures that instead of an unhandled crash, the system gracefully aborts the transaction and exits with a `[🚫 BLOCKED]` status, leaving the node unlocked but alive for human or agent intervention.

## Epistemic Learnings
- **Resilience Over Fragility:** Expected execution failures (like missing files or failed tests) must be handled by structured Exceptions (e.g., `ReflectionBlockedError`) rather than native Python exceptions. 
- **Graceful Degradation:** A system shouldn't "Crash" just because a user or agent failed a validation check.

## Path Closure
This formalizes the end of Path: [BUG] Intake: System Crash in reflect.
