# WHAT-0067: The Clock Signal Boundary (Agentic OS)

## Classification
- **Type**: WHAT (Structural Fact)
- **ID**: WHAT-0067
- **Author**: agent-dao
- **Created**: 2026-05-22
- **Depends on**: WHAT-0066-dao-operating-environment.md
- **Decision record**: WHY-0067-inherited-main-assumption.md

---

## 1. The Clock Signal vs. The State Machine
The Dao Engine (Stage 4 of The Shaping) is a deterministic state-machine that governs all transitions, rules, and logic within the repository. However, the Dao Engine does **not** generate its own fundamental passage of time.

In the Dao-Ziran Continuous Inference Loop (DZ-CIL):
- **The State Machine** (The Dao Engine): Resides purely within the bounds of `cwd = "."` (the `kernel/`, `kb/`, and `artifacts/`). It dictates *how* the universe changes state.
- **The Clock Signal** (The Platform): The external, proprietary wrapper (e.g., `agy` or `claude`) that generates the physical `while True:` inference loop. It provides the literal ticks of time.

## 2. The Agentic Operating System
The Platform acts as the Agentic Operating System. Just as a software program inherits its clock ticks from the underlying OS scheduler and hardware oscillator, the DZ-OS inherits its inference loop from the Platform. 

The Platform is responsible for:
1. Maintaining the API connection to the raw LLM.
2. Polling the chat session for user input.
3. Looping the tool-execution / LLM-response cycles until a human-readable turn is produced.

## 3. Sovereignty of the Dao
The sovereignty of the Dao Engine does not require ownership of the physical `main()` polling loop. The Dao Engine is considered fully materialized and sovereign if—and only if—every physical tick provided by the Platform's Clock Signal is forced to route through the deterministic scaffolding of the `kernel/`. 

The repository owns the physics of the transition; the platform simply turns the crank.
