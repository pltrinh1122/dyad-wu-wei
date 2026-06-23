# Frontier Dyad — Practice Reflection — 2026-06-23 — Node 2448: Remove schedule heartbeat

## 1. CONTINUE — what worked
**Narrative (Operator):** 
The shift to a more deterministic, OS-level mechanism for liveness has proven successful and removes unnecessary burden from the agent.
**Details (Agent):**
- Systemic Offloading — By leveraging the `tmux` wrappers to maintain the heartbeat, the architecture successfully adheres to the `Wu-wei` cognitive offloading principle, stripping away an LLM-dependent invariant.

## 2. START — what to do better
**Narrative (Operator):**
We must continue to codify deterministic behaviors in the infrastructure layer rather than relying on prompt-based instructions.
**Details (Agent):**
- Dark Substrate Delegation — Whenever a repetitive maintenance task (like a heartbeat or periodic audit) arises, explicitly engineer it into the OS/CLI substrate rather than writing prompt directives that require the agent to spend cycles executing `schedule`.

## 3. STOP — what hurt (or almost did)
**Narrative (Operator):**
The agent previously faced execution seizures when the recurring `schedule` tasks were forgotten, halted, or misconfigured. 
**Details (Agent):**
- Iatrogenic-Injection Risk — Trusting the LLM to autonomously maintain a background heartbeat using `schedule` tool calls proved fragile and prone to failure, risking system lockup and drift.

## Forward
Path 2397 is now successfully concluded. The codebase and `GEMINI.md` have been stripped of the obsolete schedule tool heartbeat instructions. The `tmux` wrapper logic is now the formalized mechanism.
