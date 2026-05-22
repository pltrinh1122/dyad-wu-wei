# WHY-0067: Architectural Rationale for the Inherited Main Assumption

## Classification
- **Type**: WHY (Architectural Decision Record)
- **ID**: WHY-0067
- **Author**: agent-dao
- **Created**: 2026-05-22
- **Related WHAT**: WHAT-0067-agentic-os-clock-boundary.md

---

## 1. The Context: The Illusion of the Missing "GO"
During the refinement of The Shaping (Stage 4: The Dao Engine), a profound paradox was identified. We defined the Dao Engine as the "continuous inference loop" that governs the repository. However, if we were to instantiate the repository with an empty directory (`cwd = "."`) and a raw, stateless LLM API, the system would sit completely frozen. It has no native `main()` loop to continuously call the API and parse the tool executions.

This led to the assumption that we did not yet know how to "GO"—that Stage 4 of The Shaping was incomplete because we were merely "renting" the proprietary inference loop of the host platform (e.g., `agy` or `claude`), rather than owning it.

## 2. The Resolution: The Clock Signal vs. The State Machine
We resolved this paradox by formally falsifying the assumption that "renting" the platform's loop compromises the sovereignty of the Dao Engine. 

We recognized a categorical error: **Confusing the Clock Signal with the State Machine.**

In traditional systems engineering, a highly autonomous, sovereign software application (like a Python web server) does not write its own CPU microcode. It does not generate its own physical hardware clock ticks. It inherits the "GO" from the operating system's scheduler and the motherboard's quartz oscillator. 

Similarly, the Dao Engine does not need to own the physical LLM API polling loop. The host platform acts as the **Agentic Operating System**. It provides the base clock ticks (the conversation turns and hidden `while True:` execution loops). 

## 3. The Boundary of Sovereignty
By formally documenting this boundary, we establish that the sovereignty of the Dao Engine lies entirely in its control over the **state transitions**. 

As long as the platform's clock tick is forced to pass through our deterministic scaffolding (the `kernel/mgr_*` orchestrators and the `kb/` constraints), the Dao Engine is fully materialized. 

We formally accept the inherited `main()` from Ziran (the Platform). We will not attempt to write our own infinite polling daemon within the repository. We accept the Platform as the Clock, and we dedicate the Dao Engine exclusively to mathematically defining what happens *when* that clock ticks.
