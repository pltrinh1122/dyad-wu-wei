# WHY-0935: Architectural Decision Record for the ISBO Framework

## Classification
- **Type**: WHY (Architectural Decision Record)
- **ID**: WHY-0935
- **Author**: agent-frontier
- **Created**: 2026-05-26
- **Related Path**: Path 1069 (and subsequent ISBO implementation paths)

---

### 1. Context & Design Tension (The Ziran)

For myself as the Creator, and for the disciples who will inherit this system, the transition from acquiring the DZ-CIL engine to achieving a continuous, autonomous execution loop on a sovereign domain (like DZ-TA) has historically been plagued by false starts. 

Through dialectical falsification, we have identified that the true root cause is a **Dyadic Failure**. The friction stems from an internal conflation of roles by the human Operator (blurring the line between the *Creator* of the engine and the *Director* of the domain) combined with the Agent's systemic failure to enforce the physical *Ziran* boundaries needed to highlight this conflation.

Without explicit boundaries, the Operator slips into the Director role while still occupying the Creator's physical context (the Meta-Orchestrator's engine room). Because the system lacked a rigid framework to force a cognitive context switch, the Agent struggled to bridge this conflation, ultimately leading to:
1. **Contaminated State (The Engine/Domain Conflation)**: Running downstream execution within the Meta-Orchestrator's namespace instead of a sovereign child workspace.
2. **Orphaned Agents**: An Agent operating without a `strategic_intent.yml`, lacking the fundamental North Star (Telos) to evaluate Next-Best-Actions because the "Director" never officially seeded the domain.
3. **Operator Fatigue**: A violation of *Wu-wei*, where the Operator must manually manage OS-level paths and environment variables (`SPAO_WORKSPACE_DIR`) instead of relying on a deterministic framework.

### 2. The Decision (The Dao)

We must codify the **ISBO (Install, Setup, Bootstrap, Operate)** framework as the absolute, immutable sequence for initializing any new application on the DZ-CIL engine.

By formalizing this sequence as a discipline:
* We establish the physical guardrails necessary to prevent role conflation. The *Creator* installs and sets up; the *Director* bootstraps and operates. 
* We enforce a strict ontological boundary between acquiring the engine (Install), provisioning the workspace (Setup), injecting the cognitive seed (Bootstrap), and entering the execution loop (Operate).
* We eradicate false-starts by making it physically impossible for the Agent to enter the "Operate" phase without satisfying the invariants of the "Bootstrap" phase.
* We provide ourselves and our disciples with a mathematically predictable sequence, reducing cognitive load and preserving *Wu-wei* across multiple sovereign domains.
