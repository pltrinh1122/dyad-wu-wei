# WHY-0059: Architectural Rationale for agent-SG5 Persona ID & Ownership Scope

## 1. Context & Architectural Challenge

Strategic Goal **SG-0005** (Autonomous Knowledge Accrual) requires the agent to systematically record, validate, and recall lessons learned from retrospectives and flow-state reflections without constant operator intervention. To achieve this safely and maintain system integrity, we must address three key architectural challenges:
1.  **Identity Separation**: Differentiating routine codebase changes from updates to safety guidelines, rules, and core repository ROM.
2.  **Conflict Prevention**: Ensuring that new rules synthesized or written do not contradict existing axioms, leading to cognitive deadlock.
3.  **Traceability**: Maintaining a clean, non-repudiable audit trail of who modified knowledge files and why a rule was synthesized.

Without a dedicated, explicitly tracked persona representing the owner of this strategic goal:
*   **Axiom Drift**: Any generic coding agent could modify the rules in `kb/` to bypass verification checks or resolve lint errors, weakening system constraints.
*   **Regression Loop**: The system would lack an automated way to prevent repeating similar bugs across different branches, relying on human operators to catch repeating errors.
*   **Knowledge Integrity**: There would be no designated policy custodian to guarantee that newly written guidelines are syntactically and logically consistent.

---

## 2. Rationale for Persona Isolation (`agent-SG5`)

To resolve these challenges, we introduce the formal persona ID **`agent-SG5`** as the explicit owner and custodian of SG-0005.

### 2.1 Least Privilege on Repository ROM
Isolating the knowledge base custodian from routine feature development enforces the segregation of duties. While a feature agent writes application code (e.g. database adapters or web components), `agent-SG5` owns the rules governing verification, static checking, and post-mortems. This ensures that repository ROM updates require distinct, elevated authorization.

### 2.2 Traceability of Knowledge Mutations
Requiring all files, checks, and automated synthesizers under SG-0005 to carry the `agent-SG5` identity creates a clear, traceable audit trail. If a synthesized rule causes false-positive test failures, telemetry analyzers can trace it back to the specific failure signature and resolution path approved by `agent-SG5`.

---

## 3. Rationale for Scope Boundaries

The boundaries defined in `WHAT-0059` align with the tactical goals of SG-0005:

### 3.1 Fail-State Diagnostics Parsing (`TG-0005-01`)
*   **Rationale**: Unstructured log files are difficult for models to parse reliably. Centralizing log parsing under `agent-SG5` guarantees a clean, standardized schema for tracebacks, making downstream rule synthesis deterministic and robust.

### 3.2 Knowledge Base Conflict Checking (`TG-0005-02`)
*   **Rationale**: Rule sprawl can lead to contradictions (e.g. one HOW document telling the agent to use a tool and another forbidding it). A static checker owned by `agent-SG5` guarantees that any changes to `kb/` are validated against core axioms, preventing policy pollution.

### 3.3 Automated Regression Rule Synthesis (`TG-0005-03`)
*   **Rationale**: A key risk of autonomy is repeating identical code bugs. Automating rule synthesis (writing regexes or tests from failure logs) ensures that when a bug is fixed, a test or guardrail is permanently generated to prevent its recurrence. Managing this synthesis logic belongs to `agent-SG5` to prevent feature agents from writing arbitrary, overly broad blocking rules.

### 3.4 Post-Failure Reflection Enforcement (`TG-0005-04`)
*   **Rationale**: Under pressure to complete nodes, agents might skip writing retrospective documents. By gating the `node reflect` command on the existence of post-mortem records for failed runs, `agent-SG5` programmatically ensures that learnings are never lost.

### 3.5 Contextual Prompt Injection (`TG-0005-05`)
*   **Rationale**: LLM context windows are limited, and injecting the entire `kb/` directory into every prompt causes latency and attention drift. Dynamically filtering and injecting only the relevant knowledge matching the active Path tags ensures high performance while keeping safety guidelines active.

---

## 4. Invariants & Fail-Safe Design Rationale

### 4.1 `INVARIANT_PERSONA_ISOLATION`
*   **Rationale**: Prevents spoofing. By enforcing that only processes carrying the `agent-SG5` context can run rule synthesis or conflict checks, we prevent other processes from generating unverified constraints.

### 4.2 `INVARIANT_EXCLUSIVE_LEDGER_MUTATION`
*   **Rationale**: Guarantees the integrity of safety rules. Only the designated persona can edit the rules that dictate how knowledge is updated, creating a logical barrier against unauthorized policy changes.

### 4.3 `INVARIANT_FAIL_SAFE_MUTATION`
*   **Rationale**: Standard transactional safety. If a new rule contains syntax errors or contradictions, failing the transaction preserves the last-known-good state of the repository's ROM, preventing the system from entering a broken or un-bootable state.

---

## 5. Alternative Designs Considered

### 1. Manual Knowledge Logging (Operator-Driven)
*   *Why rejected*: Relying on the human operator to manually document and check rules limits scalability and velocity (violating SG-0003). Autonomy requires the system to handle routine knowledge refinement and checking automatically.

### 2. Centralized Security Agent (Combining SG-0002 and SG-0005)
*   *Why rejected*: While sandboxing (SG-0002) and knowledge accrual (SG-0005) are both safety/governance concerns, they are orthogonal. SG-0002 focuses on compute isolation and egress, while SG-0005 focuses on learning and rules validation. Combining them would create a monolithic security agent, violating the principle of single responsibility and increasing system complexity.
