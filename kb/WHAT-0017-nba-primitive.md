# Next-Best-Action (NBA) Primitive

The **Next-Best-Action (NBA)** is a first-class primitive in the Antigravity architecture. It serves as the primary navigation mechanism for agentic execution, ensuring that the system remains aligned with the topological roadmap defined in the **Path Meta-Index**.

## 1. Role in the Sense Phase
During the **Sense** phase of the SPAO loop, the NBA orchestrator (`NBAManager`) evaluates the current environment (the `frontier_state.md`) and the repository's backlog to surface the most logical next step. This prevents the agent from deviating from the approved Path or stalling when a node is completed.

## 2. Evaluation Tiers
The NBA logic operates on a two-tier hierarchy:

| Tier | Name | Condition | Outcome |
| :--- | :--- | :--- | :--- |
| **1** | **Path Continuation** | An active Path is detected in the frontier and has pending (ready) activities in its Meta-Index. | Recommendation of child nodes within the current Path. |
| **2** | **Path Switching** | No active Path is detected OR the current Path has no ready nodes. | Recommendation of global backlog items (new Paths or unlinked Probes). |

## 3. The DAG Requirement
NBA evaluation relies on a Directed Acyclic Graph (DAG) materialized in the `Meta-Index` section of Path issues. 
- Nodes are considered **Ready** if they are incomplete and all their `[Depends: ID]` requirements are marked as `[x]`.
- Linear lists are treated as simple sequential DAGs.

## 4. Architectural Boundaries
- **Skill Layer**: Uses `gh_graph_skill.py` for stateless DAG parsing and task discovery.
- **Orchestrator Layer**: Uses `daemon_nba.py` to handle the high-level decision logic and frontier state management.
- **Sense Hooks**: Triggered automatically via `bin/node sync` to ensure the operator is always informed of the Next-Best-Action.

2. **Action Filtering**: Translates logical actions into specific CLI tool invocations based on the current context constraints.
