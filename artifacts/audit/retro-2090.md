# Frontier Dyad — Practice Reflection — 2026-06-18 — Concurrent Lock Ledger

## 1. CONTINUE — what worked
**Narrative (Operator):** We successfully migrated from a monolithic state lock to a concurrent ledger while maintaining system integrity and preserving all downstream invariants.
**Details (Agent):**
- **Surgical Refactoring** — By methodically locating where `artifacts/frontier_state/lock.json` was consumed, specifically in the Orphaned WIP CSI Guard, we were able to fully decommission the deprecated file while preserving the logical intent of the guard.
- **TDD Preservation** — Fixing `test_daemon_node.py` simultaneously with the feature code (`agent_frontier.py` and `daemon_node.py`) ensured our refactor was validated against existing assertions.

## 2. START — what to do better
**Narrative (Operator):** 
**Details (Agent):**
- **Test Context Awareness** — When changing file dependencies (like switching from `lock.json` to `frontier_state.yml`), be acutely aware that unit tests often mock `open()` or `os.path.exists()`. The tests must be updated to mock the new dependency path or helper functions.

## 3. STOP — what hurt (or almost did)
**Narrative (Operator):** 
**Details (Agent):**
- **False Invariant Breaches** — The CSI Guard began spuriously downgrading nodes because it could no longer read the monolithic lock. We must ensure that any structural refactoring of state representation is immediately accompanied by updates to the daemon guards that police that state.

## Forward
The transition to a concurrent `active_agents` ledger in `frontier_state.yml` paves the way for the Sub-Agent Dispatch architecture, allowing multiple agents to safely hold concurrent locks.
