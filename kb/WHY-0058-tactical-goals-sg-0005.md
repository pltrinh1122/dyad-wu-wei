# WHY-0058: Architectural Rationale for SG-0005 Tactical Goals

## 1. Context & Architectural Challenge

Strategic Goal **SG-0005** (Autonomous Knowledge Accrual) requires the agent to systematically record and recall lessons from past failures to avoid repeating similar errors. However, allowing an agent to autonomously modify its own knowledge base (the `kb/` directory and active guidelines) raises significant safety and engineering concerns:
1.  **Rule Contradiction (Semantic Drift)**: Autonomously generated rules or guidelines could conflict with existing system invariants, core axioms, or human operator instructions.
2.  **Structural Validation (Schema Corruption)**: Writing arbitrary documentation or instructions can introduce parsing errors in automated tooling or confuse downstream agent sessions.
3.  **Auditability & Traceability**: The human operator must be able to inspect, edit, or reject what the agent has "learned" without parsing verbose chat transcripts.
4.  **Inner-Loop Purity (Overhead)**: Large, unstructured knowledge stores or heavy semantic/vector lookups during the initialization phase can violate **SG-0003** (slowing down the TDD cycle).

To mitigate these risks while advancing the autonomy frontier, we define lightweight, structured, and statically verifiable Tactical Goals (TGs) that treat knowledge mutation as a formal code change.

---

## 2. Rationale for Tactical Goal (TG) Selection Invariants

In alignment with our system architecture, all TGs under SG-0005 must satisfy the four core validation invariants:

### 2.1 INVARIANT_TG_FALSIFIABLE_VERIFICATION (TG-Axiom 1)
*   **Rationale**: Any knowledge validation or retrieval mechanism must have a binary, testable success condition. For example, if a newly proposed guideline conflicts with a core axiom, the static validator must fail the test suite. Purely descriptive guidelines with no checking mechanisms are rejected.

### 2.2 INVARIANT_TG_DIRECT_RISK_MITIGATION (TG-Axiom 2)
*   **Rationale**: TGs must address the direct collaborative gap of human attention exhaustion. We target the specific failure mode where the operator has to repeat tactical corrections. TGs must map to concrete mechanisms that prevent repeated failures.

### 2.3 INVARIANT_TG_INNER_LOOP_PURITY (TG-Axiom 3)
*   **Rationale**: Dynamic knowledge retrieval and validation must run entirely offline in under 1 second. Heavy remote embedding generations, online model calls, or external vector store connections are prohibited during local execution loops.

### 2.4 INVARIANT_TG_ENFORCEMENT_GRADIENT (TG-Axiom 4)
*   **Rationale**: Knowledge mutation must be introduced safely. The system must support warning-only logging of rule conflicts before blocking active nodes, allowing the operator to verify learning accuracy before making blocks strict.

---

## 3. Design Decisions & Trade-Offs

### 3.1 Failure Diagnostic Parsing: Local Traceback Processing vs. Online LLM Analysis
*   **Decision**: Implement a deterministic, local parser to extract fail-state diagnostics (tracebacks, file targets, CLI errors) rather than calling an online LLM to interpret the failure in real time.
*   **Rationale**: Local log parsing is fast, offline, and produces predictable diagnostic hashes. LLM calls for failure triage introduce significant latency and flaky outputs.
*   **Trade-Off**: A local traceback parser is less flexible than an LLM and might miss complex semantic failure patterns, but it guarantees high reliability and satisfies the velocity constraint.

### 3.2 Axiom Verification: Local Syntax/Lexical Checks vs. Semantic Solvers
*   **Decision**: Enforce axiom-safety using static lexical filters, keyword matching, and structure-validated JSON/YAML schemas under the `kb/` directory, rather than executing runtime semantic solvers.
*   **Rationale**: Static syntax and pattern checks run in milliseconds, ensuring that knowledge mutations are clean, formatted correctly, and free from prohibited keywords (e.g. stale terminology).
*   **Trade-Off**: Lexical filters cannot check for deep logical contradictions, but they catch formatting errors and structural drifts instantly.

### 3.3 Regression Mitigation: Static Test Synthesis vs. Dynamic Guardrail Injection
*   **Decision**: Generate test assertions or regex rules from failure diagnostics directly into static configs (e.g. `audit_config.yml`), rather than dynamically injecting temporary rules at runtime.
*   **Rationale**: Keeping assertions static allows them to be run by the standard `pytest` harness, maintaining full test visibility and decoupling rule enforcement from the active execution session.
*   **Trade-Off**: Generating static files adds minor git index activity, but it ensures that the rules are permanent and trackable via standard commits.

### 3.4 Context Retrieval: File-Based Path Matching vs. Vector Database Lookup
*   **Decision**: Resolve and inject context by reading matching path files dynamically based on active Path/Node identifiers, rather than querying a local vector store.
*   **Rationale**: Storing knowledge in flat files linked to system paths is extremely fast and integrates with git. A vector database adds unnecessary library dependencies and runtime overhead.
*   **Trade-Off**: Path-based matching requires clear naming conventions, but it is highly predictable and has zero bootstrap latency.

---

## 4. Alternative Approaches Considered

### 1. Vector Database for Long-Term Memory (e.g., Chroma/Faiss)
*   *Why rejected*: Violates SG-0003. Setting up, indexing, and querying a vector DB locally on every command invocation introduces significant startup overhead and complicates the lightweight container setup.

### 2. Conversational Lessons (Chat History Recall)
*   *Why rejected*: Brittle and ephemeral. LLM memory fades across session truncations. Codifying lessons into version-controlled markdown/YAML is the only way to ensure permanence.
