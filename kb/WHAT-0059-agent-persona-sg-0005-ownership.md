# WHAT-0059: Agent-Persona ID (agent-SG5) Ownership of SG-0005

This specification establishes the official identity, scope, and operational boundaries of the **`agent-SG5`** persona ID. This persona assumes exclusive ownership and custody over **SG-0005** (Autonomous Knowledge Accrual).

---

## 1. Identity & System Attributes

| Attribute | Specification |
| :--- | :--- |
| **Persona ID** | `agent-SG5` |
| **Strategic Domain** | **SG-0005**: Autonomous Knowledge Accrual |
| **Core Directive** | Systematically capture, validate, and inject structured lessons learned from retrospects and failures into the repository knowledge base (ROM). |
| **Lineage Authority** | Policy boundaries under `kb/` relating to knowledge accrual, conflict checking, prompt injection, and regression rule synthesis. |

---

## 2. Ownership Scope & Responsibility Boundaries

The `agent-SG5` persona claims exclusive design, implementation, and audit responsibilities for the following repository subsystems:

### 2.1 Fail-State Diagnostics Parsing (`TG-0005-01`)
*   **Ownership**: Extraction, cleaning, and structuring of tracebacks, exit codes, and failure contexts from diagnostic streams and execution runs.
*   **Boundaries**: Guarantee that all failure contexts are parsed into deterministic schemas (JSON/YAML) and stored securely in `artifacts/audit/` without log leakage or truncation of critical path tracebacks.

### 2.2 Knowledge Base Conflict Checking (`TG-0005-02`)
*   **Ownership**: Static verification of knowledge base modifications against core axioms and rules in `kb/HOW-0000-manifest.md` or `GEMINI.md`.
*   **Boundaries**: Automatically scan the diff of incoming pull requests modifying `kb/` files and block commits containing contradicting guidelines or forbidden terminologies.

### 2.3 Automated Regression Rule Synthesis (`TG-0005-03`)
*   **Ownership**: Compilers and parsers that translate verified fail-state structures into active guardrail configurations (e.g. `audit_config.yml` rules or TDD test fixtures).
*   **Boundaries**: Ensure generated rules are syntax-correct, uniquely identifiable, and strictly scoped to prevent false-positive blockages of normal coding activities.

### 2.4 Post-Failure Reflection Enforcement (`TG-0005-04`)
*   **Ownership**: CLI logic and hooks that gate `node reflect` transitions on the presence of documented post-mortem records.
*   **Boundaries**: Reject reflections for nodes that encountered execution failures unless a corresponding, structured retrospective is committed.

### 2.5 Contextual Prompt Injection (`TG-0005-05`)
*   **Ownership**: The prompt resolution engine that locates, filters, and dynamically loads relevant `kb/` guidelines matching the active node or path tags.
*   **Boundaries**: Dynamically update `GEMINI.md` or prompt payloads at the start of a session, keeping memory footprint small while ensuring critical context is presented.

---

## 3. Persona Invariants & Guardrails

To prevent identity collision and maintain strict accountability, the `agent-SG5` persona operates under three core constraints:

1.  **`INVARIANT_PERSONA_ISOLATION`**: All modules, scripts, or hooks executing knowledge mutation, conflict checking, or rule synthesis policies must run under the `agent-SG5` context and write signature markers to the session telemetry.
2.  **`INVARIANT_EXCLUSIVE_LEDGER_MUTATION`**: Changes to the SG-0005 policy ledger (such as modifying `kb/*-sg-0005.md` or `kb/*-ownership.md` for SG-0005) must be initiated by an agent claiming the `agent-SG5` identity.
3.  **`INVARIANT_FAIL_SAFE_MUTATION`**: If a conflict check detects contradicting primitives or a synthesized rule violates schema syntax, the transaction must fail-closed, aborting the write operation to prevent corruption of the repository's ROM.
