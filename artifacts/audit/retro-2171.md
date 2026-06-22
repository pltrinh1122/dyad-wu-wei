# Retrospective - Node 2171

**Bug Intake:** System Crash in reflect
**Description:** The reflect phase crashed due to an unhandled exception (`FileNotFoundError` or `ReflectionBlockedError` when local invariants like `enforce_reflection_hook` failed).
**Root Cause:** Instead of a graceful exception mapping into `[🚫 BLOCKED]`, the native exception bubbled up and crashed the daemon, forcing an ungraceful system termination and leaving the node locked.
**Remediation:** Node 2182 caught `ReflectionBlockedError` directly within `node_lifecycle.py` so the transaction is aborted gracefully and the node exits with a `[🚫 BLOCKED]` status instead of a full traceback crash.

**Epistemic Principles:**
- **Graceful Degradation:** The daemon must not crash because a local test or invariant failed; it should cleanly roll back and block the transaction.
