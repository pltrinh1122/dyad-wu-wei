# WHAT-0060: Tactical Goals for SG-0001 Backlog Dynamics and Resource Budget Harmonization

This document defines the Tactical Goals (TGs) that realize **SG-0001** (Backlog Dynamics and Resource Budget Harmonization). These goals provide concrete engineering milestones to dynamically harmonize backlog selection with the operator's strategic intent ledger.

---

## 1. Tactical Goal Invariants & Axioms

To maintain the architectural rigor of the metasystem, any Tactical Goal (TG) selected under a Strategic Goal (SG) must satisfy the following four validation invariants:

1.  **`INVARIANT_TG_FALSIFIABLE_VERIFICATION` (TG-Axiom 1)**:
    *   *Ontology*: A TG must define a binary, deterministic, programmatically testable constraint. If the system fails to satisfy the constraint (e.g., executing a non-prioritized path or exceeding resource budgets), verification must fail or halt the loop.
    *   *Requirement*: The definition must include a concrete, automated check that can fail.

2.  **`INVARIANT_TG_DIRECT_RISK_MITIGATION` (TG-Axiom 2)**:
    *   *Ontology*: A TG must directly mitigate a specific execution or harmonization risk that prevents the operator from delegating backlog prioritization authority (e.g., resource budget waste, attention drift, orphaned nodes, or incorrect path ranking).
    *   *Requirement*: The goal must map directly to a component of the parent Strategic Goal's collaborative gap.

3.  **`INVARIANT_TG_INNER_LOOP_PURITY` (TG-Axiom 3)**:
    *   *Ontology*: The prioritization, ranking, or tracking controls defined by the TG must not introduce performance overhead that violates the execution limits of **SG-0003** (i.e., local validation tests must complete completely offline in under 60 seconds).
    *   *Requirement*: Latency overhead of backlog and budget checks must remain negligible (<100ms).

4.  **`INVARIANT_TG_ENFORCEMENT_GRADIENT` (TG-Axiom 4)**:
    *   *Ontology*: The TG must support a gradient of enforcement (e.g., from `dry-run / notify` to `strict enforcement / block`) to allow the operator to tune the gate threshold based on safety telemetry.
    *   *Requirement*: The goal's implementation must reference or expose a configuration setting to dial enforcement levels.

---

## 2. Tactical Goal Registry (SG-0001)

Applying the invariants above, we define four tactical milestones:

### TG-0001-01: Deterministic Prioritization Evaluator
*   **Definition**: Restrict active execution nodes to paths that are explicitly mapped in the `prioritized_paths` section of active goals in `strategic_intent.yml`.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Directly mitigates the risk of executing off-goal paths and wasting resource/token budget on tasks that the operator has not prioritized.
    *   *Verification Metric*: A validation check must query `strategic_intent.yml` and verify that the target path ID is explicitly prioritized under an active Strategic Goal. If not, the system must log a harmonization violation.
    *   *Inner-Loop Purity*: Negligible overhead via local YAML lookup (<5ms).
    *   *Enforcement Gradient*: Configuration parameter to toggle between logging a warning and hard-blocking node start.
*   **Backlog Mapping**: Path 560 (Activity 563 - Reflect - Codify SG-0001 Tactical Goals and Persona Domain Ownership)

### TG-0001-02: Next-Best-Action (NBA) Dynamic Re-ranking
*   **Definition**: Dynamically rank backlog nodes in the SENSE phase according to active strategic goal weights and prioritized path references.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Resolves the "attention drift" collaborative gap by automatically bubble-sorting prioritized path nodes to the top of the NBA selection list.
    *   *Verification Metric*: The NBA scorer must score and sort prioritized path nodes higher than non-prioritized nodes, testable via unit tests.
    *   *Inner-Loop Purity*: Local ranking logic executes in <10ms.
    *   *Enforcement Gradient*: Supports configurable weights for prioritized vs. routine backlog items.
*   **Backlog Mapping**: Path 560 (Activity 563)

### TG-0001-03: Resource and Token Budget Monitoring
*   **Definition**: Measure and bound resource expenditure (tokens, API calls, elapsed time) per path to prevent budget exhaustion on a single path.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Prevents runaway execution loops or excessive resource spend on lower-priority paths.
    *   *Verification Metric*: The execution loop must log resource consumption per path and alert or halt when consumption exceeds configured thresholds.
    *   *Inner-Loop Purity*: Writing usage stats to local telemetry takes <1ms.
    *   *Enforcement Gradient*: Configurable budget thresholds per path; support warnings vs hard halts.
*   **Backlog Mapping**: Path 560 (Activity 563)

### TG-0001-04: Path Harmonization Validator
*   **Definition**: Statically validate that any newly registered backlog path has a corresponding mapping to a Strategic Goal ID (`strategic_intent.yml`).
*   **Invariance Matching**:
    *   *Risk Mitigation*: Prevents orphaned nodes or untracked paths from entering the backlog, maintaining strict traceability.
    *   *Verification Metric*: The backlog factory tool must fail to generate or prioritize a path if it is not mapped to an active Strategic Goal ID.
    *   *Inner-Loop Purity*: Local validation check runs in <20ms.
    *   *Enforcement Gradient*: Supports warning during creation vs blocking registration.
*   **Backlog Mapping**: Path 560 (Activity 563)

---

## 3. Implementation Traceability Matrix

The tactical goals are designed to map directly to current and future backlog Path activities:

| Tactical Goal | Backlog Node | Description | Status |
| :--- | :--- | :--- | :--- |
| **TG-0001-01** | Node 563 | Reflect - Codify SG-0001 Tactical Goals and Persona Domain Ownership | Backlog |
| **TG-0001-02** | Node 563 | Reflect - Codify SG-0001 Tactical Goals and Persona Domain Ownership | Backlog |
| **TG-0001-03** | Node 563 | Reflect - Codify SG-0001 Tactical Goals and Persona Domain Ownership | Backlog |
| **TG-0001-04** | Node 563 | Reflect - Codify SG-0001 Tactical Goals and Persona Domain Ownership | Backlog |
