# WHY-2027: Harmonize "GEMINI.md changed" Bug Intake

## 1. The Phenomenon
When the Operator modifies `GEMINI.md` or `AGENT.md`, the `audit_daemon.py` detects the modification via the `file_modified` rule. It then constructs a `[FAILURE]` alert and routes it through `dispatch_alert()`. Because `dispatch_alert()` hardcodes the `[BUG] Intake:` prefix for all alerts, it spawns an orphan Path in the backlog (e.g., `[BUG] Intake: GEMINI.md changed — agent (/exit) recommended`).

## 2. The Fallacy
1. **Ontological Conflation**: A change to the System Prompt (`GEMINI.md`) is a purposeful Dao evolution driven by the Operator, not a defect in the system's execution logic. Categorizing it as a `[BUG]` pollutes the problem space.
2. **Execution Waste**: Spawning a Backlog Path forces the Agentic Loop to later pick up the `[BUG]` node, checkout a worktree, and attempt to "remediate" a file change that requires no remediation. This violates the Preservation of Autonomous Velocity (SG-0003).
3. **Improper Alert Routing**: The `dispatch_alert()` function blindly maps every alert (including `[NOTIFICATION]`) to a `[BUG]` intake, stripping the original semantic severity.

## 3. The Resolution (Philosophical Intent)
Operational directives (like a system prompt reload) must trigger a **HARD HALT** to prevent the Agent from operating under stale invariants (Iatrogenic hazard). However, this halt should be a **stateless interrupt**, not a **stateful backlog mutation**. 
The daemon should emit the alert to `stdout` (to interrupt the agent) and optionally exit with a non-zero code to break the `SPAOR` loop, but it MUST NOT dispatch a DAG node for file-modification reload events. Furthermore, `dispatch_alert` itself must be refactored to respect the semantic `alert_level` (e.g. `[WARN]`, `[ALERT]`) rather than defaulting to `[BUG]`.
