# WHY-0057: Architectural Rationale for agent-SG2 Persona ID & Ownership Scope

## 1. Context & Architectural Challenge

Strategic Goal **SG-0002** (Gateless Autonomous Execution within Risk-Managed Sandbox) requires the system to safely execute codebase mutations and system commands without a constant human review gate. To achieve this, the repository must possess clear, non-repudiable policies governing:
1. What mechanisms enforce compute and network sandbox boundaries.
2. How execution logs are verified as authentic and tamper-proof.
3. Which system components have authorization to change sandbox policy configurations.

Without a dedicated, explicitly tracked persona representing the owner of this strategic goal:
* **Identity Drift**: Any generic agent could execute modifications to security-critical sandbox parameters without clear accountability.
* **Auditability Gaps**: Logs and PR metadata would not differentiate between routine application-level changes and sensitive system-level policy alterations.
* **State Coherence**: There would be no designated policy custodian to verify that all active nodes satisfy the safety invariants of SG-0002.

---

## 2. Rationale for Persona Isolation (`agent-SG2`)

To resolve these challenges, we introduce the formal persona ID **`agent-SG2`** as the explicit owner of SG-0002. 

### 2.1 Identity Decoupling
Decoupling the sandbox custodian from the routine coding agent enforces the principle of least privilege at the logical architecture layer. While a coding agent implements feature logic, `agent-SG2` owns the execution envelope itself. This ensures that security boundaries are treated as first-class, immutable definitions.

### 2.2 Traceability and Non-Repudiation
By requiring all SG-0002 policy commits, pull requests, and telemetry payloads to carry the `agent-SG2` persona ID, we establish a clean, non-repudiable audit trail. If a sandbox violation occurs, telemetry analyzers can trace the exact policy state authorized by the persona.

---

## 3. Rationale for Scope Boundaries

The boundaries defined in `WHAT-0057` map directly to the six tactical goals of SG-0002:

### 3.1 Compute & Process Containment (`TG-0002-01`)
* **Rationale**: Defining limits (memory, CPU, timeout) is a core security concern. Assigning this to `agent-SG2` guarantees that execution timeouts and quotas cannot be dynamically disabled or weakened by application-level code without triggering a policy violation.

### 3.2 Network Egress Containment (`TG-0002-02`)
* **Rationale**: Network exfiltration is the primary channel for credential theft and unauthorized data leakage. By isolating the allowlist and network namespace configuration under `agent-SG2`, we prevent unverified network access.

### 3.3 Idempotent Git State Recovery (`TG-0002-03`)
* **Rationale**: Autonomy requires a guaranteed "undo" button. Placing git rollback logic under `agent-SG2` ensure that if a run fails, the cleanup routine is executed with elevated verification priority, leaving zero orphaned files.

### 3.4 Skill-Level Lexical Guardrails (`TG-0002-04`)
* **Rationale**: Static analysis prevents "escape commands" (e.g. bypassing adapter wrappers via raw python `subprocess` calls). The rules of the Lexical Guard must be managed by the safety persona to prevent coding agents from adding unsafe bypass patterns.

### 3.5 Non-Repudiable Logs & Audit Trails (`TG-0002-05`)
* **Rationale**: The integrity of audit trails is paramount. If log generation could be modified by the executing agent, a malicious or buggy loop could erase its own footprint. `agent-SG2` maintains the cryptographic or structural schema of these logs.

### 3.6 Dynamic Gating & Autonomy Control (`TG-0002-06`)
* **Rationale**: The transition from manual gates to autonomous gates is the ultimate transition point of the metasystem. Managing the schema and state transitions of `gates.yml` belongs to `agent-SG2` to ensure the gradient is adjusted according to proven safety metrics.

---

## 4. Invariants & Fail-Safe Design Rationale

### 4.1 `INVARIANT_PERSONA_ISOLATION`
* **Rationale**: Prevents persona collision. If any agent could arbitrarily claim to act as `agent-SG2`, the accountability model collapses.

### 4.2 `INVARIANT_EXCLUSIVE_LEDGER_MUTATION`
* **Rationale**: Hardens the policy files. Only the persona holding the SG-0002 mandate is permitted to modify files that dictate safety rules, creating a strict cryptographic or logical barrier.

### 4.3 `INVARIANT_FAIL_SAFE_CONTAINMENT`
* **Rationale**: High-reliability engineering dictates that in the event of a boundary breach, the system must fail-closed rather than fail-open. Halting execution prevents cascading failures or data leakage before the operator can intervene.

---

## 5. Alternative Designs Considered

### 1. Monolithic Agent Persona (Single Identity)
* *Why rejected*: A single monolithic agent would perform both application development and security policy configuration. This lacks segregation of duties, making it difficult to verify if a security bypass was introduced accidentally during feature development.

### 2. Physical Container Segregation (Virtual Machines Only)
* *Why rejected*: While physically isolating executions in separate VMs provides strong security, it introduces high latency and violates SG-0003. Decoupling the persona logically allows us to enforce policies at the repository/VCS level while maintaining high execution speed.
