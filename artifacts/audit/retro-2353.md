# Frontier Dyad — Practice Reflection — 2026-06-22 — Node 2353

## 1. CONTINUE — what worked
**Narrative (Operator):** Relocating the swarming mechanics out of the Antigravity-specific GEMINI.md file strengthens the engine core.
**Details (Agent):**
- The relocation structurally formalizes the Portability Axiom. The engine itself now knows about concurrent factory floor mechanics rather than it being a shim applied by GEMINI.md. This ensures symmetric capabilities across different dyadic instantiations.

## 2. START — what to do better
**Narrative (Operator):** Let's ensure bug paths are handled properly moving forward.
**Details (Agent):**
- Dispatch full `[BUG]` paths directly to subagents for execution instead of manually planning them node by node, to keep the strategist seat free for high-level tasks.

## 3. STOP — what hurt (or almost did)
**Narrative (Operator):** The reflect script crashes when required files don't exist in the new workflow.
**Details (Agent):**
- We experienced `node_lifecycle.py` crashing due to `git add` attempting to track `artifacts/frontier_state.md` which had been removed in previous nodes. The script has been hotfixed on `main` to dynamically check file presence before staging, preventing such brittle execution failures.

## Forward
The new swarm fan-out mechanics are codified natively within DYAD.md. We are ready to ingest new BUG paths efficiently.
