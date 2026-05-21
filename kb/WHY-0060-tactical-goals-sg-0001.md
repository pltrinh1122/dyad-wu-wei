# WHY-0060: Architectural Rationale for SG-0001 Tactical Goals

## 1. Context & Architectural Challenge

Strategic Goal **SG-0001** (Backlog Dynamics and Resource Budget Alignment) requires that the agent's backlog selection is dynamically mapped to the operator's high-level intent, preventing attention drift and ensuring resources are spent efficiently. However, establishing this alignment raises several architectural challenges:
1.  **Attention Drift**: Without dynamic prioritization, the agent may pick backlog items that are disconnected from the operator's current active focus.
2.  **Resource Contention/Waste**: The agent has a finite resource budget (tokens, time, API calls). Spending budget on off-goal paths reduces system utility and increases cost.
3.  **Backlog Bloat**: Unaligned or orphaned paths can enter the backlog, making prioritization difficult and introducing noise.
4.  **Enforcement Balance**: If prioritization is too rigid, the agent cannot handle emergent issues or exploratory tasks (probes). If too loose, budget is wasted.

To address these challenges, we establish clear tactical goals (TGs) guided by strict invariants to ensure the backlog remains aligned with strategic intent.

---

## 2. Rationale for Tactical Goal (TG) Selection Invariants

To maintain architectural rigor, all tactical goals for SG-0001 must satisfy four selection invariants:

### 2.1 INVARIANT_TG_FALSIFIABLE_VERIFICATION (TG-Axiom 1)
*   **Rationale**: Any prioritization mechanism must be programmatically verifiable. If the scorer, budget tracker, or alignment checker cannot be tested programmatically, we cannot rely on it to enforce compliance. Every TG must define a binary test check.

### 2.2 INVARIANT_TG_DIRECT_RISK_MITIGATION (TG-Axiom 2)
*   **Rationale**: We must not add arbitrary backlog filtering rules that do not map to the active strategic intent. Every TG must directly mitigate the risk of resource waste or attention drift.

### 2.3 INVARIANT_TG_INNER_LOOP_PURITY (TG-Axiom 3)
*   **Rationale**: Backlog scanning and scoring must not slow down the SENSE phase or inner-loop tests. Heavy external queries or slow network scans are prohibited; all checks must evaluate local state (YAML files) in under 100ms.

### 2.4 INVARIANT_TG_ENFORCEMENT_GRADIENT (TG-Axiom 4)
*   **Rationale**: The operator must have control over the alignment strictness. A configurable gradient allows the operator to toggle between warning alerts and hard blocks depending on the active development mode.

---

## 3. Design Decisions & Trade-Offs

### 3.1 Prioritization Verification: Strict Path Blocking vs. Dynamic Scoring
*   **Decision**: Implement a deterministic evaluator (`TG-0001-01`) combined with a dynamic NBA re-ranking scorer (`TG-0001-02`).
*   **Rationale**:
    *   *Strict Path Blocking*: Only allows execution of paths in `prioritized_paths`. While this completely eliminates resource waste on off-goal paths, it prevents the agent from addressing urgent hotfixes or minor adjustments.
    *   *Dynamic Re-Ranking*: Bubble-sorts prioritized items to the top while allowing other items to be selected if no prioritized items remain.
*   **Trade-Off**: We combine both by introducing a configurable enforcement parameter, giving the operator the flexibility to decide when to enforce strict boundaries.

### 3.2 Resource Tracking: Active Limiting vs. Post-Hoc Analysis
*   **Decision**: Track resource and token budgets at the path level and update local telemetry on every node reflection (`TG-0001-03`).
*   **Rationale**: Real-time token tracking inside the inner loop adds complexity and overhead. Recording usage metrics during the reflect phase and validating against limits on node initialization provides a robust, low-overhead solution.
*   **Trade-Off**: Running limits post-hoc means a single node could theoretically overrun the budget before being blocked, but this is mitigated by node-level execution timeouts.

### 3.3 Backlog Governance: Restricting Backlog Registration vs. Free Creation
*   **Decision**: Statically validate that any newly registered backlog path has a corresponding mapping to a Strategic Goal ID (`TG-0001-04`).
*   **Rationale**: Preventing orphaned nodes at the point of creation ensures the backlog remains clean and structured, rather than running periodic clean-up scripts.
*   **Trade-Off**: This forces the developer/operator to always specify a strategic mapping during backlog generation, but it guarantees 100% traceability.

---

## 4. Alternative Approaches Considered

### 1. Manual Path Selection (Operator Picks Every Node)
*   *Why rejected*: Violates the North Star collaboration gap by keeping the operator tightly coupled to low-level execution planning, causing decision fatigue.

### 2. Full Dynamic RL-based Backlog Prioritization
*   *Why rejected*: Introduces high complexity, is non-deterministic, and violates the inner-loop purity invariant due to the latency and compute requirements of runtime model inference.
