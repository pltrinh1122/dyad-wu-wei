# WHY-0048: Rationale for NBA Scoring Rubric

## 1. Context & Motivation

Historically, next-best-actions (NBAs) were recommended based on heuristic sequences and manual backlog listings. This approach lacked quantitative verification, making it difficult to audit why specific nodes were selected over others. 

To bridge this gap and establish a foundation for the concurrent **Auditor Agent**, we require a formal, mathematical rubric to calculate an objective score for every potential transition.

## 2. Design Rationale

### 2.1. Multiplicative Dependency Gate
We chose a multiplicative dependency gate ($C_{\text{Dependency}}$) rather than a simple additive score. If a node's dependencies are open, its prioritization must be strictly $0.00$, regardless of how strategically valuable or safe it is. An additive model could allow a high-strategic-value node to be selected even if it is blocked, violating execution ordering laws.

### 2.2. Weight Distribution
The weights are distributed to prioritize **Compliance** and **Strategic Utility** equally ($0.40$ each), while allocating $0.20$ to **Operational Risk**.
* **Compliance ($0.40$)**: Ensures the agent stays within the boundaries of the repository's rules (e.g. WIP-N=1, testing invariants).
* **Strategic Utility ($0.40$)**: Guarantees alignment with the operator's active strategic goals.
* **Operational Risk ($0.20$)**: Acts as a tie-breaker, favoring safer, less complex nodes to optimize flow velocity.

### 2.3. North-Star Alignment (NS)
The ultimate North-Star (NS) of this repository is a state of fully autonomous execution where hard, blocking gates are replaced by dynamic, self-regulating feedback loops. The rubric provides the mathematical engine necessary to rank actions dynamically, enabling the system to evaluate its own decisions without hard-coded state limits.
