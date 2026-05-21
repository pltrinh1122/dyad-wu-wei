# Post-Failure Retrospective: Node 599

**Node**: Probe 599 — Audit SG ownership coverage and gap analysis for WHAT-0062  
**Path**: 591 (578-A: Codify Persona Ownership as ROM Primitives)  
**Date**: 2026-05-21  
**Authored by**: agent-SG5

---

## Failure Events Recorded

Two execution failures were recorded in telemetry against Node 599 during this session:

1. **`plan-start 599` — State Dissonance**: The frontier's `current_active_node` was set to the descriptive string `"(none — awaiting plan-start on Path 591)"` instead of a true null value. The purity check interpreted this as an existing active node lock and blocked plan-start.

2. **`set_active_node` via `frontier_editor`**: Initial call used the wrong null representation; required a second call with the literal string `"None"` to trigger the null branch in `mgr_frontier.set_active_node`.

---

## Root Cause

When performing the frontier hotfix (switching from Path 299 → Path 591), the active node was set to a human-readable placeholder string rather than `None`. The `_verify_state_purity` check in `node_lifecycle.py` reads the raw YAML value and raises `State Dissonance` if it is truthy — any non-empty string, including a descriptive placeholder, is treated as an occupied lock.

---

## Corrective Actions Taken

- Called `mgr_frontier.set_active_node(fp, "None")` to properly null the pointer.
- Plan-start succeeded on the second attempt.
- Probe executed successfully; 200/200 tests pass; gap report committed.

---

## Lessons / Feedforward Invariants

1. **Frontier null representation**: The only valid "no active node" value is Python `None` / YAML `null`. Any string, even descriptive, is treated as a lock. Document this in `kb/HOW-0001` or the `bin/node abort` implementation (Activity #586).
2. **Hotfix frontier mutations must use `"None"` string**: When clearing the active node via `mgr_frontier.set_active_node`, always pass `"None"` (string) — this triggers the `if node_name == "None" or node_name is None` null branch.
3. **`bin/node abort` would have prevented this entirely**: A proper abort primitive (Activity #586, Path 292) would have atomically nulled the frontier in one safe operation without the two-step hotfix sequence.
