# WHY-0011: The Soft-Locking Principle

## Decision
We utilize a "Soft-Locking" mechanism for Node concurrency (e.g., preserving the `backlog` label and applying a `status: in-progress` label that yields a warning instead of a hard exception) rather than enforcing strict programmatic blocks.

## Rationale
1. **Agentic Autonomy**: A core principle of the Antigravity architecture is that **agents should ensure prerequisites before execution**. Hard-locking mechanisms at the CLI level force rigid workflows that can paralyze agents when state synchronization issues occur (e.g., GitHub API eventual consistency).
2. **Fair Warning vs. Rigid Blocking**: By printing a bright yellow warning and continuing automatically, we provide the agent with "fair warning" that a Node is currently under evaluation or in progress. This allows an informed decision while trusting the agent's logic to handle concurrent overlap, rather than prematurely crashing the execution loop.
3. **Backlog Visibility**: Preserving the `backlog` label during evaluation ensures the Node remains visible in the queue until it is formally completed and closed via the Reflect phase. This prevents Nodes from disappearing into a hidden "in-progress" state, improving overall system observability.
