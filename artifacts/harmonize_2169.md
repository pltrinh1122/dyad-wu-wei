# Harmonization: [BUG] Intake: System Crash in reflect

## 1. Issue Overview
Node 2169 addresses a system crash reported during the `reflect` subcommand of the node lifecycle. The crash manifests as an unhandled Python traceback rather than a clean validation block.

## 2. Root Cause Analysis
- The `reflect` phase invokes `daemon_knowledge_accrual.enforce_reflection_hook(self.issue_id, ...)`.
- If the hook determines that reflection is blocked (e.g., due to SG-0005 requiring a post-mortem reflection record after failures), it raises a `ReflectionBlockedError`.
- Because the `reflect` method in `kernel/node_lifecycle.py` does not catch `ReflectionBlockedError`, the exception propagates up to `daemon_node.py` and causes an unhandled Python crash.
- This creates an Iatrogenic "System Crash" in the telemetry and issue tracker, obscuring the fact that it is a legitimate validation block.

*Note: Older tracebacks (e.g., in Node 1830) indicated an `UnboundLocalError` for `main_repo`, but the underlying structural issue is identical: validation checks throwing unhandled exceptions instead of terminating cleanly with `sys.exit`.*

## 3. Philosophical Intent & Technical Resolution
**Intent:**
The system must enforce invariant blocks gracefully. When a Node is blocked from reflecting (whether due to CI failures, merge conflicts, or missing reflection records), the daemon must notify the agent via standard error (using `sys.exit("[🚫 BLOCKED] ...")`) rather than crashing entirely. 

**Technical Plan:**
In `kernel/node_lifecycle.py` within the `reflect()` method, wrap the call to `enforce_reflection_hook` in a `try/except` block that catches `ReflectionBlockedError`. When caught, it should invoke `sys.exit(f"[🚫 BLOCKED] {str(e)}")` to terminate execution smoothly and signal the agent properly.

## 4. Pre/Post-Requisites
- **Pre-requisite:** None.
- **Post-requisite:** Implement the exception catch in `kernel/node_lifecycle.py`.

## 5. End State
The `reflect` command will fail cleanly with a `[🚫 BLOCKED]` message when the reflection hook rejects the transition, rather than emitting a traceback and triggering false "System Crash" issues.
