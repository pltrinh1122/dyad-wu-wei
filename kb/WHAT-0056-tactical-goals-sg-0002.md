# WHAT-0056: Tactical Goals for SG-0002 Sandbox Hardening

This document defines the Tactical Goals (TGs) that realize **SG-0002** (Gateless Autonomous Execution within Risk-Managed Sandbox). These goals provide concrete engineering milestones to eliminate manual operator review gates while ensuring execution safety.

---

## 1. Tactical Goal Invariants & Axioms

To maintain the architectural rigor of the metasystem, any Tactical Goal (TG) selected under a Strategic Goal (SG) must satisfy the following four validation invariants:

1.  **`INVARIANT_TG_FALSIFIABLE_VERIFICATION` (TG-Axiom 1)**:
    *   *Ontology*: A TG must define a binary, deterministic, programmatically testable constraint. If the system fails to satisfy the constraint (e.g., an execution timeout, network connection attempt, or uncommitted files), the system must halt or fail verification.
    *   *Requirement*: The definition must include a concrete, automated check that can fail.

2.  **`INVARIANT_TG_DIRECT_RISK_MITIGATION` (TG-Axiom 2)**:
    *   *Ontology*: A TG must directly mitigate a specific execution or containment risk that prevents the operator from granting autonomous execution authority (e.g., CPU/memory exhaustion, network exfiltration, workspace state pollution, or untraceable edits). Aesthetic clean-ups or modularity improvements alone do not qualify as TGs.
    *   *Requirement*: The goal must map directly to a component of the parent Strategic Goal's collaborative gap.

3.  **`INVARIANT_TG_INNER_LOOP_PURITY` (TG-Axiom 3)**:
    *   *Ontology*: The security, containment, or tracking controls defined by the TG must not introduce performance overhead that violates the execution limits of **SG-0003** (i.e., local validation tests must complete completely offline in under 60 seconds). Heavy containerization loops or synchronous remote checks are prohibited.
    *   *Requirement*: Latency overhead of isolation controls must remain negligible (e.g., systemd namespaces, local git trees).

4.  **`INVARIANT_TG_ENFORCEMENT_GRADIENT` (TG-Axiom 4)**:
    *   *Ontology*: The TG must support a gradient of enforcement (e.g., from `dry-run / notify` to `strict enforcement / block`) to facilitate gradual, risk-tiered operator un-gating. Autonomy is not a binary toggle; the operator must be able to tune the gate threshold based on observed safety telemetry.
    *   *Requirement*: The goal's implementation must reference or expose a configuration setting to dial enforcement levels.

---

## 2. Tactical Goal Registry (SG-0002)

Applying the invariants above, we define six tactical milestones:

### TG-0002-01: Sandboxed Compute Containment
*   **Definition**: Restrict the compute footprint of agent-spawned commands to prevent resource starvation, denial-of-service, or escape from the designated workspace.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Prevents CPU starvation, infinite loops, and memory-based DOS.
    *   *Verification Metric*: Any command exceeding configured limits (e.g., 2GB memory, 2 CPU cores, 10-second timeout) must be terminated automatically, and its status must be logged as a resource violation.
    *   *Inner-Loop Purity*: Negligible overhead via OS process containment.
    *   *Enforcement Gradient*: Configurable timeout/memory parameters; supports warning-only alerts before hard kills.
*   **Backlog Mapping**: Path 292 (Activity 295 - Enforce Adapter Execution Invariants)

### TG-0002-02: Network Egress Containment
*   **Definition**: Establish a strict egress allowlist for all agent-spawned network processes, blocking unauthorized connections.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Prevents data exfiltration and unauthorized external command/control connections.
    *   *Verification Metric*: Network requests to domains outside the allowlist must be blocked at the system or socket level, throwing a `NetworkSandboxException`.
    *   *Inner-Loop Purity*: Socket filtering adds zero latency to offline execution.
    *   *Enforcement Gradient*: Whitelist configurable via environment files; supports dry-run telemetry logging.
*   **Backlog Mapping**: Path 292 (Activity 295)

### TG-0002-03: Idempotent Git State Recovery
*   **Definition**: Ensure the agent can always restore the git working tree to a clean, known-good state if test execution fails, an invariant is broken, or a transaction aborts.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Prevents filesystem contamination, ghost edits, and dirty worktrees.
    *   *Verification Metric*: Any rollback command must restore the repository state (untracked, modified, or deleted files) to the baseline commit within 5 seconds with zero residual untracked files.
    *   *Inner-Loop Purity*: Standard git recovery operations run in <200ms.
    *   *Enforcement Gradient*: Automatic recovery toggled per transaction boundary.
*   **Backlog Mapping**: Path 292 (Activity 294 - Implement Idempotent PR Management)

### TG-0002-04: Skill-Level Lexical Guardrails
*   **Definition**: Validate that the agent's code modifications adhere to structural and import purity rules (e.g., forbidding direct usage of raw subprocesses in `drivers/`, enforcing telemetry wrappers).
*   **Invariance Matching**:
    *   *Risk Mitigation*: Blocks the agent from bypassing skills wrappers to execute arbitrary shell commands.
    *   *Verification Metric*: The static analysis gate must flag and reject any commit modifying `drivers/` that uses `subprocess` directly instead of wrapping it via `drivers.git_client` or designated runner drivers.
    *   *Inner-Loop Purity*: AST scanning executes in under 50ms.
    *   *Enforcement Gradient*: Custom regex patterns and warnings configurable in `audit_config.yml`.
*   **Backlog Mapping**: Path 292 (Activity 295)

### TG-0002-05: Non-Repudiable Execution Logging & Audit Trails
*   **Definition**: Generate structured, tamper-proof audit trail payloads for every execution session, detailing the exact commands run, resources consumed, and sandbox policies triggered.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Eliminates the risk of untraceable modifications or hidden execution failures.
    *   *Verification Metric*: The system must write a signed or checksummed MD/JSON payload to `artifacts/audit/` at the end of each session, verifying that the actual execution matches the plan contract.
    *   *Inner-Loop Purity*: File writes introduce negligible overhead.
    *   *Enforcement Gradient*: Configurable logging verbosity levels.
*   **Backlog Mapping**: Path 292 (Activity 296 - Generalize Telemetry Test-Safety)

### TG-0002-06: Operator-Configurable Autonomy Control (Dynamic Gating)
*   **Definition**: Establish a dynamic, schema-validated configuration layer enabling the operator to selectively ungate specific transition steps (e.g., SENSE to PLAN, PLAN to ACT, or ACT to REFLECT) based on path risk level and sandbox status.
*   **Invariance Matching**:
    *   *Risk Mitigation*: Resolves the "all-or-nothing" trust bottleneck by allowing gradual, tiered un-gating.
    *   *Verification Metric*: The execution engine must block unauthorized execution of downstream steps if corresponding configurations in `gates.yml` require manual HITL approval, testable via unit tests.
    *   *Inner-Loop Purity*: Simple YAML schema parsing adds <5ms overhead.
    *   *Enforcement Gradient*: Supports transitions from manual approve/deny (`enforce`), to warning notify (`dry-run`), to full automation (`gateless`).
*   **Backlog Mapping**: Path 472 (Operator Configurable Gate Enforcement)

---

## 3. Implementation Traceability Matrix

The tactical goals are designed to map directly to current and future backlog Path activities:

| Tactical Goal | Backlog Node | Description | Status |
| :--- | :--- | :--- | :--- |
| **TG-0002-01** | Node 295 | Enforce Adapter Execution Invariants | Backlog |
| **TG-0002-02** | Node 295 | Enforce Adapter Execution Invariants | Backlog |
| **TG-0002-03** | Node 294 | Implement Idempotent PR Management | Backlog |
| **TG-0002-04** | Node 295 | Enforce Adapter Execution Invariants | Backlog |
| **TG-0002-05** | Node 296 | Generalize Telemetry Test-Safety | Backlog |
| **TG-0002-06** | Node 472 | Operator Configurable Gate Enforcement | Backlog |
