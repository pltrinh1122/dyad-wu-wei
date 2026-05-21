# WHY-0063: Architectural Rationale for Platform Domain Tactical Goals

This document explains the architectural and philosophical rationale behind the Tactical Goals (TGs) defined in `WHAT-0063` for the Platform Domain.

---

## 1. Why a "Platform" Domain Instead of an SG?

Historically, the repository conflated system *domains* (structural software boundaries) with *Strategic Goals* (human-agent collaboration outcomes). This created a category error where cross-cutting infrastructure had no logical home without violating the `INVARIANT_PERSONA_ISOLATION` constraint. 

By defining the Platform Domain horizontally, we achieve true **Domain-Driven Design (DDD)**. The Platform Domain does not solve a single strategic gap on its own; instead, it is the underlying communication substrate (the message bus, the locking mechanisms, the CLI parser) that makes it mathematically possible to execute the isolated logic of SG-0001 (Prioritization), SG-0002 (Sandboxing), and SG-0005 (Knowledge Accrual).

## 2. Rationale for TG-PLAT-01: Agent-to-Agent Handoff Schemas (a2ai)
*   **The Problem**: When `agent-SG5` completes its static ROM indexing, `agent-SG2` must consume it to build a runtime gate. If the hand-off schema is vague or conversational, `agent-SG2` will misinterpret the dependencies and trigger a sandbox violation.
*   **The Solution**: We enforce strict JSON/YAML schemas and Markdown node templates.
*   **The Trade-off**: This increases the boilerplate required to create an inter-agent Path contract. However, in an autonomous metasystem, **determinism is always prioritized over brevity**. Strict typing at the agent boundary prevents cascading failures that require human debugging.

## 3. Rationale for TG-PLAT-02: DAG Concurrency Lock Enforcement (a2ai)
*   **The Problem**: Multiple agents executing asynchronously will eventually attempt to transition or mutate the same topological node or path (e.g., two agents trying to `plan-start` the same backlog issue).
*   **The Solution**: The Platform Domain owns the concurrency locks (`skills/file_locker.py`), establishing a single source of truth for execution state.
*   **The Trade-off**: File-based locking introduces minimal latency and a theoretical risk of stale locks if an agent hard-crashes. This is mitigated by robust timeout implementations and atomic locking mechanisms, which are strictly preferable to version control collisions in the artifacts tree.

## 4. Rationale for TG-PLAT-03: Operator Intent Parser (o2ai)
*   **The Problem**: Operator intent is high-level ("build a UI widget"), but the system requires mathematically strict, multi-domain Path Contracts (e.g., Path A for SG5, Path B for SG2) to maintain domain isolation.
*   **The Solution**: The Platform Domain acts as a compiler, translating conversational intent into strictly formatted, DAG-linked GitHub backlog issues.
*   **The Trade-off**: The system requires an interactive conversational interface to perform this compilation, but by pushing this into the horizontal `o2ai` pillar, we keep the vertical backend agents pure and stateless.

## 5. Rationale for TG-PLAT-04: Asynchronous Prompt Ingestion (o2ai)
*   **The Problem**: Operators need to instruct the system dynamically, but forcing an active sandbox agent to pause execution to read a chat message breaks inner-loop velocity (SG-0003).
*   **The Solution**: A dedicated ingestion queue (`artifacts/prompt_backlog.yml`) that can be polled safely between execution boundaries.
*   **The Trade-off**: Adds an asynchronous delay between when the operator types a command and when the backend agent acknowledges it. This is considered acceptable because the metasystem prioritizes safe, gateless execution over synchronous reactivity.
