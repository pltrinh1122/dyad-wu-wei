# WHY-0085: Agent ROM Drift Safeguard

## The Premise
The Agentic Architecture (WHAT-0001) dictates that the Agent is instantiated as a state machine whose entire operational identity and boundaries (its ROM) are defined by the `GEMINI.md` system prompt. 

When the local agent synchronizes its repository with `origin/main` via the `sync` command (Sense Phase), it pulls down the latest code and documentation. If the system prompt (`GEMINI.md`) was mutated in `main`, the physical repository reflects the new invariants, but the currently executing Agent instance retains the *stale* invariants loaded into its ROM at startup.

## The Problem
Executing under a stale ROM creates an epistemic fracture between the physical system state and the Agent's cognitive boundaries. The Agent will proceed to Plan, Act, and Reflect using rules that are obsolete or completely contradictory to the newly fetched `GEMINI.md`. This violates the Absolute Invariance of the Audit Ledger and introduces chaotic unpredictability into the state machine.

## The Invariant (The Safeguard)
To prevent invariant violations caused by stale instructions, the Meta-Orchestrator enforces a hard **ROM Drift Safeguard**. 

During the `sync` execution, the system must deterministically verify if `GEMINI.md` has changed via SHA-256 hash comparison. If a drift is detected, the Orchestrator MUST emit a highly visible terminal gate (a CRITICAL ROM DRIFT banner) that explicitly warns the Operator to forcefully terminate and restart the Agent instance (`agy`), guaranteeing synchronization between the Meta-Orchestrator's physical invariants and the Agent's injected ROM.
