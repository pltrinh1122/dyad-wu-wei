# WHAT-0063: Tactical Goals for Platform Domain Enablement

This document defines the Tactical Goals (TGs) that realize the **Platform Domain**. Unlike standard domains that map 1-to-1 to a Strategic Goal (SG), the Platform Domain provides horizontal enablement for multiple goals (e.g., SG-0001, SG-0002, SG-0004, SG-0005) by abstracting Agent-to-Agent (a2ai) and Operator-to-Agent (o2ai) interfaces.

---

## 1. Tactical Goal Invariants & Axioms

To maintain the architectural rigor of the metasystem, any Tactical Goal (TG) selected under the Platform Domain must satisfy the following four validation invariants:

1.  **`INVARIANT_TG_FALSIFIABLE_VERIFICATION` (TG-Axiom 1)**:
    *   *Ontology*: A TG must define a binary, deterministic, programmatically testable constraint.
    *   *Requirement*: The definition must include a concrete, automated check that can fail.

2.  **`INVARIANT_TG_DIRECT_RISK_MITIGATION` (TG-Axiom 2)**:
    *   *Ontology*: A TG must directly mitigate a specific execution or harmonization risk (e.g., race conditions, schema drift, human decision fatigue).
    *   *Requirement*: The goal must map directly to a cross-cutting collaborative gap.

3.  **`INVARIANT_TG_INNER_LOOP_PURITY` (TG-Axiom 3)**:
    *   *Ontology*: The platform interfaces defined by the TG must not introduce performance overhead that violates the execution limits.
    *   *Requirement*: Latency overhead of parsing or concurrency locks must remain negligible.

4.  **`INVARIANT_TG_ENFORCEMENT_GRADIENT` (TG-Axiom 4)**:
    *   *Ontology*: The TG must support a gradient of enforcement to allow tuning.
    *   *Requirement*: The goal's implementation must expose configuration for enforcement levels.

---

## 2. Tactical Goal Registry (Platform Domain)

Applying the invariants above, we define four tactical milestones for the Platform Domain:

### TG-PLAT-01: Strict Agent-to-Agent Handoff Schemas (a2ai)
*   **Definition**: Establish deterministic, statically verified payload schemas (JSON/YAML) and Node Contract templates (`kb/templates/`) for all cross-agent state transfers.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Mitigates schema drift and misinterpretation when executing dependent nodes, ensuring downstream agents do not fail due to malformed upstream outputs.
    *   *Verification Metric*: Schema validators must fail the execution transition if the serialized state does not match the structural type constraints.
    *   *Inner-Loop Purity*: Local schema validation completes in <10ms.
    *   *Enforcement Gradient*: Can be tuned from structural warnings to hard execution halts.

### TG-PLAT-02: DAG Concurrency Lock Enforcement (a2ai)
*   **Definition**: Enforce rigorous concurrency control mechanisms (`drivers/file_locker.py`) and topological checks during node state transitions.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Prevents race conditions, orphaned processes, and corrupted state when multiple agents attempt to access or modify the same topological frontier concurrently.
    *   *Verification Metric*: Attempts to mutate a locked node or a node missing prerequisite closures must raise an immediate deterministic exception.
    *   *Inner-Loop Purity*: File-based locking resolves in <2ms.
    *   *Enforcement Gradient*: Configurable timeout limits and retry-backoff algorithms.

### TG-PLAT-03: Operator Intent Parser (o2ai)
*   **Definition**: Translate conversational, high-level operator directives into mathematically strict, multi-node Path Contracts injected directly into the backlog.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Solves the "decision fatigue" gap by abstracting the verbose creation of GitHub issues away from the human operator.
    *   *Verification Metric*: The parser must successfully generate valid, correctly formatted `bin/backlog new` execution calls mapping to the human's requested domain.
    *   *Inner-Loop Purity*: Local template generation executes fully offline.
    *   *Enforcement Gradient*: Gracefully degrades by prompting the operator for clarification if intent cannot be mapped to a known schema.

### TG-PLAT-04: Asynchronous Prompt Ingestion (o2ai)
*   **Definition**: Manage the polling, parsing, and structured flushing of operator prompt queues (`artifacts/prompt_backlog.yml`) without blocking active agent sandboxes.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Prevents the operator from being blocked by a running agent while attempting to queue future intent.
    *   *Verification Metric*: The ingestion queue must successfully dequeue and transition prompt objects into backlog issues or state mutations without causing concurrent write collisions.
    *   *Inner-Loop Purity*: Background ingestion tasks must consume minimal CPU overhead.
    *   *Enforcement Gradient*: Supports queuing limits and rate-limiting configurations.

### TG-PLAT-05: Agent-Driven Workspace Materialization (o2ai)
*   **Definition**: Enable Operators (Vibe Coders) to initialize new Wu-wei Dyad workspaces natively through Agent prompts and Template Repositories, eliminating rigid manual `curl` installation scripts.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Solves the "installation friction" gap by allowing the conversational agent (or native GitHub features) to perform the scaffolding sequence, honoring the Wu-wei Gate for AI-native operators.
    *   *Verification Metric*: The Agent must successfully scaffold the `.workspace/` directory and its required invariants purely from an initialization prompt or template, bypassing legacy `curl` installers.
    *   *Inner-Loop Purity*: Eliminates the need for external network script dependencies (`curl | bash`) from the operator's onboarding loop.
    *   *Enforcement Gradient*: Supports graceful fallback to the manual CLI wrapper (`bin/workspace init`) if conversational context is unavailable.
