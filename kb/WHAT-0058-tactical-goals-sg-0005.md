# WHAT-0058: Tactical Goals for SG-0005 Autonomous Knowledge Accrual

This document defines the Tactical Goals (TGs) that realize **SG-0005** (Autonomous Knowledge Accrual). These goals provide concrete engineering milestones to enable the agent to systematically record, validate, and recall lessons from past failures.

---

## 1. Tactical Goal Invariants & Axioms

To maintain the architectural rigor of the metasystem, any Tactical Goal (TG) selected under a Strategic Goal (SG) must satisfy the following four validation invariants:

1.  **`INVARIANT_TG_FALSIFIABLE_VERIFICATION` (TG-Axiom 1)**:
    *   *Ontology*: A TG must define a binary, deterministic, programmatically testable constraint. If the system fails to satisfy the constraint (e.g., an invalid YAML format, a rule conflict, or missing reflection logs), verification must fail.
    *   *Requirement*: The definition must include a concrete, automated check that can fail.

2.  **`INVARIANT_TG_DIRECT_RISK_MITIGATION` (TG-Axiom 2)**:
    *   *Ontology*: A TG must directly mitigate a specific execution or containment risk that prevents the operator from granting autonomous execution authority (e.g., repeated code bugs, stale terminology regressions, or semantic configuration conflicts).
    *   *Requirement*: The goal must map directly to a component of the parent Strategic Goal's collaborative gap.

3.  **`INVARIANT_TG_INNER_LOOP_PURITY` (TG-Axiom 3)**:
    *   *Ontology*: The security, containment, or tracking controls defined by the TG must not introduce performance overhead that violates the execution limits of **SG-0003** (i.e., local validation tests must complete completely offline in under 60 seconds).
    *   *Requirement*: Latency overhead of knowledge validation and retrieval must remain negligible (<100ms).

4.  **`INVARIANT_TG_ENFORCEMENT_GRADIENT` (TG-Axiom 4)**:
    *   *Ontology*: The TG must support a gradient of enforcement (e.g., from `dry-run / notify` to `strict enforcement / block`) to facilitate gradual, risk-tiered operator un-gating.
    *   *Requirement*: The goal's implementation must reference or expose a configuration setting to dial enforcement levels.

---

## 2. Tactical Goal Registry (SG-0005)

Applying the invariants above, we define five tactical milestones:

### TG-0005-01: Automated Fail-State Diagnostics Parser
*   **Definition**: Parse and format fail-state diagnostics (tracebacks, file references, exited commands, and exit codes) upon test or sync failures into structured diagnostic schemas.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Resolves the risk of missing critical debugging signatures or failure conditions by programmatically structuring failure contexts.
    *   *Verification Metric*: A parser must extract fail tracebacks and output a valid JSON/YAML structure, testable via unit tests checking output against mock error tracebacks.
    *   *Inner-Loop Purity*: Negligible overhead via raw local string processing.
    *   *Enforcement Gradient*: Supports silent logging of diagnostics vs. blocking the loop if diagnostics cannot be parsed.
*   **Backlog Mapping**: Path 541 (Activity 544 - Implement Autonomous Knowledge Accrual Engine)

### TG-0005-02: Knowledge Base Conflict Checking
*   **Definition**: Statically validate that newly added rules, guidelines, or instructions in the `kb/` directory do not violate core axioms (e.g., `kb/HOW-0000-manifest.md` or `GEMINI.md` invariants).
*   **Invariance Matching**:
    *   *Risk Mitigation*: Prevents semantic conflicts and guidelines contradictions from drifting into the ROM of the agent.
    *   *Verification Metric*: A validator script must scan the repository diff for `kb/` changes and fail if forbidden keywords or contradicting instructions are detected.
    *   *Inner-Loop Purity*: AST and text scanning runs in <50ms.
    *   *Enforcement Gradient*: Supports warnings during checks (`dry-run`) vs. blocking `node plan-finish` on failure (`strict`).
*   **Backlog Mapping**: Path 541 (Activity 544)

### TG-0005-03: Automated Regression Rule Synthesizer
*   **Definition**: Automatically synthesize lexical guardrail rules or test assertions from validated failure diagnostics and write them into the configuration ledger.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Prevents the agent from repeating the same code or naming mistakes across different branches.
    *   *Verification Metric*: An automated rule synthesizer must successfully translate a fail-state signature into a regex rule in `audit_config.yml` or a new lexical check assertion.
    *   *Inner-Loop Purity*: Parsing and appending config files executes in under 20ms.
    *   *Enforcement Gradient*: Supports warning notifications in the terminal vs. hard test failures.
*   **Backlog Mapping**: Path 541 (Activity 544)

### TG-0005-04: Mandatory Post-Failure Reflection Hook
*   **Definition**: Enforce that a structured post-mortem reflection record is compiled and committed if the active loop undergoes recovery or debugging repair cycles.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Ensures lessons are permanently documented and not skipped during fast troubleshooting cycles.
    *   *Verification Metric*: The `node reflect` command must verify that if a node has recorded any failure telemetry, a corresponding retrospective markdown file exists under `artifacts/audit/`.
    *   *Inner-Loop Purity*: Simple directory/file existence check takes <1ms.
    *   *Enforcement Gradient*: Supports prompting the operator for sign-off vs. failing the reflect command.
*   **Backlog Mapping**: Path 541 (Activity 544)

### TG-0005-05: Contextual Prompt Injector
*   **Definition**: Resolve and dynamically inject relevant knowledge guidelines (such as `kb/WHAT-*` or `kb/WHY-*` files matching the active path scope) into the agent's system prompt context.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Minimizes agent context drift by surfacing highly specific, relevant rules for the active work target.
    *   *Verification Metric*: A prompt builder script must resolve active Path tags, locate matching files under `kb/`, and inject them into `GEMINI.md` or the runtime configuration.
    *   *Inner-Loop Purity*: Running a regex/glob path resolver adds <5ms latency.
    *   *Enforcement Gradient*: Configurable injection severity (none, matching files, full kb).
*   **Backlog Mapping**: Path 541 (Activity 544)

---

## 3. Implementation Traceability Matrix

The tactical goals are designed to map directly to current and future backlog Path activities:

| Tactical Goal | Backlog Node | Description | Status |
| :--- | :--- | :--- | :--- |
| **TG-0005-01** | Node 544 | Implement Autonomous Knowledge Accrual Engine | Backlog |
| **TG-0005-02** | Node 544 | Implement Autonomous Knowledge Accrual Engine | Backlog |
| **TG-0005-03** | Node 544 | Implement Autonomous Knowledge Accrual Engine | Backlog |
| **TG-0005-04** | Node 544 | Implement Autonomous Knowledge Accrual Engine | Backlog |
| **TG-0005-05** | Node 544 | Implement Autonomous Knowledge Accrual Engine | Backlog |
