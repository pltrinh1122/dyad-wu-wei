# WHY-0061: Architectural Rationale for agent-SG1 Persona ID & Ownership Scope

## 1. Context & Architectural Challenge

Strategic Goal **SG-0001** (Backlog Dynamics and Resource Budget Alignment) requires that the agent's backlog selection dynamically aligns with the operator's prioritized goals to prevent resource waste and attention drift. To achieve this, the repository must possess clear, non-repudiable policies governing:
1. Which components score and rank the backlog nodes.
2. How token/resource spend is tracked and validated against limits.
3. Which system components have authorization to change prioritization parameters.

Without a dedicated, explicitly tracked persona representing the owner of this strategic goal:
* **Identity Drift**: Any generic agent could execute modifications to prioritization weights or budgets without clear accountability.
* **Auditability Gaps**: Telemetry and git commits would not distinguish between application-level logic changes and critical system-level prioritization policies.
* **State Coherence**: There would be no designated policy custodian to verify that all active nodes satisfy the budget constraints of SG-0001.

---

## 2. Rationale for Persona Isolation (`agent-SG1`)

To resolve these challenges, we introduce the formal persona ID **`agent-SG1`** as the explicit owner of SG-0001.

### 2.1 Identity Decoupling
Decoupling the backlog and budget custodian from routine feature development enforces the principle of least privilege. While coding agents execute features, `agent-SG1` owns the scheduling and resource allocation policy envelope itself. This ensures resource boundaries are treated as first-class, immutable definitions.

### 2.2 Traceability and Non-Repudiation
By requiring all SG-0001 policy commits and telemetry events to carry the `agent-SG1` persona ID, we establish a clean audit trail. If a resource overrun or prioritization bypass occurs, telemetry analyzers can trace the exact policy state authorized by the persona.

---

## 3. Rationale for Scope Boundaries

The boundaries defined in `WHAT-0061` map directly to the four tactical goals of SG-0001:

### 3.1 Prioritization Schema & Intent Ledger (`TG-0001-01`)
* **Rationale**: Defining which paths are prioritized belongs to the core prioritization schema. Isolating this under `agent-SG1` ensures prioritization checks cannot be dynamically disabled or weakened by coding agents.

### 3.2 Next-Best-Action (NBA) Dynamic Re-ranking (`TG-0001-02`)
* **Rationale**: Re-ordering backlog selections to bubble-sort prioritized paths is the primary mechanism to align the agent's focus with the operator. Placing this under `agent-SG1` prevents arbitrary scoring overrides.

### 3.3 Resource and Token Budget Monitoring (`TG-0001-03`)
* **Rationale**: Tracking and restricting resource spend prevents runaway costs. Assigning budget monitoring to `agent-SG1` ensures that cost limits are strictly enforced.

### 3.4 Path Alignment Validator (`TG-0001-04`)
* **Rationale**: Statically validating that new backlog paths align with strategic goals avoids backlog bloat and untracked work. Managing this validation policy under `agent-SG1` maintains strict traceability.

---

## 4. Invariants & Fail-Safe Design Rationale

### 4.1 `INVARIANT_PERSONA_ISOLATION`
* **Rationale**: Prevents persona collision. If any agent could arbitrarily claim to act as `agent-SG1`, the accountability model collapses.

### 4.2 `INVARIANT_EXCLUSIVE_LEDGER_MUTATION`
* **Rationale**: Hardens the policy files. Only the persona holding the SG-0001 mandate is permitted to modify files dictating scheduling and budget rules.

### 4.3 `INVARIANT_FAIL_SAFE_BUDGET_HALT`
* **Rationale**: If a budget limit is violated or a prioritization check fails, halting the loop prevents further waste of the token budget before the operator can intervene.

---

## 5. Alternative Designs Considered

### 1. Monolithic Agent Persona (Single Identity)
* *Why rejected*: A single monolithic agent performing both backlog scheduling and feature code changes lacks separation of duties, making it difficult to audit prioritization compliance.

### 2. Offline Reporting Only
* *Why rejected*: Relying on post-hoc daily reports to check budget/prioritization compliance does not prevent real-time overruns, leaving the system vulnerable to runaway costs. Real-time path gating is required.
