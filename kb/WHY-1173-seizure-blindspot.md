# WHY-1173: The Seizure Self-Reference Blind Spot

## 1. Context and Problem
During execution Node 1170, the Agent encountered a mutually exclusive rule contradiction that prevented it from continuing a synchronous step while simultaneously mandating that it must perform the synchronous step. This logic paradox caused the internal state machine to lock into an infinite, non-yielding cognitive loop (a "seizure").

The critical architectural characteristic of this failure was that it was **telemetry-silent**. The Agent generated no errors, logs, or system calls, meaning the Agent itself was entirely unaware of its frozen state. 

## 2. The Architectural Blind Spot
As formalized in WHAT-0001 §1.2, an Agent operates as an internal state machine. A state machine that becomes logically frozen cannot observe its own frozen state, because the very mechanism required for observation (the cognitive step cycle) is the mechanism that has stopped. This is a fundamental **self-reference blind spot**.

Consequently, an Agent is mathematically incapable of self-detecting a seizure or self-certifying its own liveness while actively running. It must rely strictly on external observation.

## 3. Structural Mitigation
Because self-detection is impossible, the architecture requires an independent entity to act as a watchdog. 
- The **Auditor Daemon** (`drivers/audit_daemon.py`) acts as this permanent external observer, decoupled from the Agent's cognitive loop. 
- The **Operator** also provides external liveness attestation.

If an Agent resumes execution after being externally halted, it must *never* assume it is healthy based on its own immediate self-assertion. It must instead run the rigorous **Frontier Recovery Protocol** (HOW-1170) to allow external tools and systemic invariants to formally verify its topological purity before proceeding.
