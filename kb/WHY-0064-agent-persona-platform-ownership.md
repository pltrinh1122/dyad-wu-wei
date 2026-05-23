# WHY-0064: Architectural Rationale for agent-ziran Persona ID & Ownership Scope

This document details the architectural reasoning and strategic justification for establishing the `agent-ziran` persona.

---

## 1. The Category Error of Persona-to-SG Coupling

In the initial bootstrapping of the metasystem, personas were mapped on a 1-to-1 basis with Strategic Goals (e.g., `agent-SG1` owned SG-0001). While this forced strict accountability, it exposed a fatal architectural flaw when dealing with cross-cutting infrastructure:
*   If `agent-SG5` needs to send a diagnostic payload to `agent-SG2`, who owns the structure of that payload? 
*   If `agent-SG2` defines it, `agent-SG5` violates `INVARIANT_PERSONA_ISOLATION` by mutating an SG2 schema. 
*   If `agent-SG5` defines it, the inverse is true.

**The Rationale**: We must decouple Personas (system actors) from Strategic Goals (metrics of success). Personas must map to **Software Domains**, not Strategic Goals. The `agent-ziran` persona exists to resolve this category error by claiming exclusive ownership over the horizontal "Shared Kernel" (the `platform` domain) that enables all other vertical domains to communicate.

## 2. Segregation of Duties: o2ai and a2ai

The decision to explicitly divide the Platform Domain into `o2ai` (Operator-to-Agent) and `a2ai` (Agent-to-Agent) pillars provides necessary specialization:
*   **o2ai** deals with *Human Asynchrony*: The human operator is slow, conversational, and non-deterministic. The `agent-ziran` acting in an `o2ai` capacity acts as a translator, buffering the noise of human interaction and converting it into strict Backlog Contracts.
*   **a2ai** deals with *Machine Determinism*: Once the human intent is compiled into the backlog, the `a2ai` pillar takes over to ensure that when `agent-SG5` finishes a node, it cleanly releases a lock so `agent-SG2` can pick up the next node.

## 3. The `INVARIANT_DOMAIN_AGNOSTICISM` Guardrail

The `agent-ziran` persona is bound by `INVARIANT_DOMAIN_AGNOSTICISM`.
*   **The Rationale**: If the platform team (or platform agent) starts writing business logic (e.g., deciding *which* specific terms are banned by SG-0005), it creates tight coupling. The platform must remain purely structural. It provides the `WHAT/WHY` template; `agent-SG5` fills it in. It provides the `drivers/file_locker.py` utility; `agent-SG1` calls it. By restricting `agent-ziran` from owning business logic, we guarantee that the communication layer remains pristine and highly reusable across any future SGs.
