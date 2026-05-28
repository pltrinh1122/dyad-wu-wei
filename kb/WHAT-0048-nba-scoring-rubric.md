# WHAT-0048: Next-Best-Action (NBA) Scoring Rubric

This specification defines the formal mathematical rubric and scoring taxonomy used to compute the prioritization index of potential agent transitions (Nodes) in the repository's backlog.

## 1. The prioritisation Equation

For any pending Node $V$, the Next-Best-Action prioritization score $S_{\text{NBA}}(V) \in [0.00, 1.00]$ is computed using a multiplicative dependency gate combined with a weighted sum of compliance, strategic utility, and operational safety:

$$S_{\text{NBA}}(V) = C_{\text{Dependency}}(V) \times \left( 0.40 \times C_{\text{Axiom}}(V) + 0.40 \times C_{\text{Strategic}}(V) + 0.20 \times C_{\text{Risk}}(V) \right)$$

Where:
* $C_{\text{Dependency}}(V) \in \{0.0, 1.0\}$ represents the node's readiness constraint.
* $C_{\text{Axiom}}(V) \in [0.0, 1.0]$ represents compliance with system axioms.
* $C_{\text{Strategic}}(V) \in [0.0, 1.0]$ represents strategic harmonization.
* $C_{\text{Risk}}(V) \in [0.0, 1.0]$ represents risk and concurrency mitigation.

---

## 2. Dimension Definitions

### 2.1. Dependency Gate ($C_{\text{Dependency}}$)
Assesses whether the node is logically unblocked.
* **`1.0` (Ready)**: All pre-requisite issues and parent nodes are merged and completed.
* **`0.0` (Blocked)**: At least one pre-requisite or parent issue remains open.

### 2.2. Axiomatic Compliance ($C_{\text{Axiom}}$)
Assesses harmonization with the system's structural laws.
* **`1.0` (Perfect)**: Strictly complies with standard execution models (e.g. Discovery Harmonize -> Discovery Plan -> Activity Reflect) and operates in isolated worktrees.
* **`0.5` (Minor Drift)**: Touches global infrastructure or changes shared tooling configuration files, requiring minor validation checks.
* **`0.0` (Violation)**: Directly violates core guardrails (e.g. violates WIP-N=1, bypasses PR reviews, or attempts raw/un-wrappered git/gh operations).

### 2.3. Strategic Harmonization ($C_{\text{Strategic}}$)
Assesses relevance to the active strategic goals.
* **`1.0` (Highest)**: Directly traces to a prioritized strategic goal inside `strategic_intent.yml`.
* **`0.5` (Indirect)**: Non-prioritized backlog task that resolves technical debt or improves local workflows.
* **`0.0` (Out of Scope)**: Orphaned task with no relation to repository evolution.

### 2.4. Operational Risk ($C_{\text{Risk}}$)
Assesses resource costs and execution safety.
* **`1.0` (Low Risk)**: Low code-footprint, executes completely offline, and poses zero thread/lock contention risks.
* **`0.5` (Medium Risk)**: Poses potential file-locking conflicts or touches directories shared with other concurrent agents.
* **`0.0` (High Risk)**: Requires manual operator credentials, changes local daemon processes, or can lead to network calls during TDD loops.
