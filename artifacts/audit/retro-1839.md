# Frontier Dyad — Practice Reflection — 2026-06-07 — Node 1839 (Discard Invariant Guard)

## 1. CONTINUE — what worked
**Narrative (Operator):** 
**Details (Agent):**
- Systematically creating tests alongside mechanistic guards — Ensured the Discard Invariant guard was falsifiable by mocking `subprocess` carefully.

## 2. START — what to do better
**Narrative (Operator):**
**Details (Agent):**
- Mocking environment dependencies properly — Must remember that local imports within a function require patching the module at the top level or mocking correctly to prevent execution side effects (like running real git commands in the workspace).

## 3. STOP — what hurt (or almost did)
**Narrative (Operator):**
**Details (Agent):**
- Unintended Side Effects in Falsification — The `test_sync_and_clean_node_wip_violation` caused the test suite to execute against the real filesystem because the mock fell through on `subprocess.check_output`, triggering the guard and aborting the test runner with `SystemExit: 1`.

## Forward
The Discard Invariant Guard is fully mechanized. The system now effectively intercepts destructive sync operations when uncommitted tracked edits exist, returning a steering vector instead of silently dropping state. The node can now be safely reflected.
