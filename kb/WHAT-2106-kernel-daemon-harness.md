# WHAT-2106: Kernel Daemon Harness (The Loop Rewire)

## 1. Intent & Problem Statement
The Main Agent (`kernel_daemon` / `frontier`) was historically tasked with executing all low-level `Act` nodes by default when it triggered the autonomous loop (`bin/status` auto-lock). As the system scales toward true multi-agent parallelism, this "executor instinct" creates a cognitive bottleneck and violates the principle of separation between strategic management and low-level execution.

The intent of Path 2106 is to wire the Next-Best-Action (NBA) dispatcher such that the Main Agent is exclusively confined to Administrative domains (Harmonize, Plan, Reflect), while Execution domains (`Act`) are delegated strictly to subagents. 

## 2. Theoretical Falsification
The previous workflow posited that the single Agent can efficiently toggle between strategic design (WHY/WHAT) and deep implementation details (HOW/Execution).
*Falsification*: This conflates contexts and clutters the Main Agent's context window, increasing Token Usage and decreasing Systemic Durability. Separation of concerns at the agent level (Dyadic/Management vs Execution) is strictly required.

## 3. The Re-Wired NBA Loop
The execution loop is modified as follows:
1. `bin/status` surfaces the NBA from the DAG.
2. The `auto_resolve_persona` logic classifies the node:
   - If the node is `Harmonize`, `Plan`, `Reflect`, `Align`, `Activity`, or `Discovery`, it is strictly assigned to `frontier`.
   - If the node is `Act`, it proceeds to standard domain ownership lookup (`WHAT-0065`, e.g., `agent-sg5`).
3. `bin/status` executes `plan-start <NBA_ID>`, acquiring the lock for the assigned persona.
4. `bin/status` prints the dispatch output. If assigned to a subagent, it emits a specific signal instructing the Main Agent to `invoke_subagent`.
5. The Main Agent's system instructions (`GEMINI.md`) compel it to dispatch execution nodes to subagents via `invoke_subagent`, rather than checking out and executing them itself.

## 4. Sub-Nodes (DAG)
- **Node 2107**: Harmonize - Design the Loop Rewire dispatch protocol.
- **Node 2108**: Plan - Lock the specification and create the `Act` implementation node.
- **Node 2141**: Act - Implement the auto-resolve logic, the `bin/status` print modifications, and update the `GEMINI.md` system prompt.
- **Node 2109**: Reflect - Validate the loop rewire logic.
