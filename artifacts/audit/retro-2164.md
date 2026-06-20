# Frontier Dyad — Practice Reflection — 2026-06-20 — Path 2164: Re-architecture of Path Container State Preservation

## 1. CONTINUE — what worked
**Narrative (Operator):** The decision to shift from text-based checkbox tracking to the actual GitHub API state resolved the long-standing bug of phantom path generation and DAG seizure.
**Details (Agent):**
- System robustness — `gh_graph_skill.py` directly queries GitHub for the source of truth, sidestepping out-of-sync markdown checkboxes entirely. This aligns with the "Substrate Abstraction" goal.

## 2. START — what to do better
**Narrative (Operator):** We should be more decisive about executing the Harmonize and Plan nodes associated with a Path when dispatching them to sub-agents or executing them autonomously, rather than trying to execute the wrapper Path container.
**Details (Agent):**
- Execute actual children nodes — `plan-start` must operate on the actionable leaf nodes of a Path (like the Plan and Harmonize phases) rather than halting or auto-locking the parent container issue. This ensures fluid transition to Act delegation.

## 3. STOP — what hurt (or almost did)
**Narrative (Operator):** Acquiring an exclusive `current_active_node` lock on a non-actionable Path issue stalled execution because it obscured the next actual tasks and prevented the system from advancing to the actual `Harmonize` and `Plan` actions without manual intervention.
**Details (Agent):**
- Locking container nodes — The Agent must be careful not to execute or lock abstract wrapper issues (Path) natively. `daemon_nba.py` handles expanding the Path into actionable children, which correctly avoids this anti-pattern.

## Forward
The Path Container architecture is now stabilized, and DAG states accurately reflect remote truth. Next, we will continue demonstrating the "Concurrent Factory Floor" pattern with the updated routing behavior.
