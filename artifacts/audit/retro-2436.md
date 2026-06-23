# Frontier Dyad — Practice Reflection — 2026-06-23 — Path 2399 (Persistent Session Wrappers)

## 1. CONTINUE — what worked
**Narrative (Operator):** The structural move to wrap the daemon execution in a bash script managed by tmux finally frees the LLM from acting as a process supervisor. The introduction of `bin/agy.sh` and `bin/claude.sh` realizes the "Dark Substrate" ideal—machinery that enforces invariants without taking up cognitive space.
**Details (Agent):**
- Systemic Robustness — By running `audit_daemon.py` in an infinite loop inside `tmux` and wiring crash dumps directly to `gh issue create`, the loop handles failures asynchronously without LLM polling or seizure.
- True Dormancy — The agent is no longer forced to manually invoke `manage_task(kill)` and re-schedule cron tasks upon waking up. This permanently eliminates the "heartbeat seizure" class of failures.

## 2. START — what to do better
**Narrative (Operator):** We should begin standardizing these external wrappers across all dyad instantiations so that local environments automatically boot with the daemon running correctly.
**Details (Agent):**
- Substrate Initialization — Ensure new workspace instantiations automatically trigger or verify the `tmux` session rather than relying on manual operator script execution.

## 3. STOP — what hurt (or almost did)
**Narrative (Operator):** Trying to use the agent's tool-calling layer to supervise long-lived daemons created chronic instability.
**Details (Agent):**
- Iatrogenic-Injection Risk — Relying on ephemeral LLM memory to maintain background schedules led to overlapping cron jobs and execution seizures. Moving the responsibility to the OS layer solves this natively.

## Forward
The persistent session wrappers (`bin/agy.sh`, `bin/claude.sh`) effectively terminate the daemon-supervision requirement for the LLM. Path 2399 is complete. We will now close Path 2399 and update our instructions.
