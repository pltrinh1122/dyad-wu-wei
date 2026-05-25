# WHY-0635: Concurrent Agent State Awareness

## The Context
The Antigravity Metasystem is evolving from a single-threaded orchestration model into an orthogonally parallel multi-agent system. Each domain (e.g., `agent-meta`, `agent-platform`, `agent-ziran`) can execute its own Sense-Plan-Act-Observe loops concurrently. 

However, the topological ledger (`artifacts/frontier_state.yml`) historically used singleton pointers:
```yaml
current_active_path: null
current_active_node: null
```

## The Conflict
When multiple agents operate concurrently, they check out their respective nodes. If `agent-meta` checks out Node A, and `agent-platform` simultaneously checks out Node B, the singleton pointers will be overwritten by whichever agent acted last. This leads to state-pointer hallucination, where an agent's topological location is lost or stolen by a parallel process. While `skills/file_locker.py` prevents OS-level file contention during writes, it does not prevent logic-level semantic overwrites of the singleton pointer.

## The Architectural Resolution
To resolve this, the `frontier_state.yml` schema must transition from a singleton paradigm to a multi-tenant matrix paradigm keyed by the agent's unique Persona ID (`SPAO_PERSONA_ID`):

```yaml
active_agents:
  agent-meta:
    current_active_path: "Issue #100: Path 100..."
    current_active_node: "Node 101: Activity 101..."
  agent-platform:
    current_active_path: "Issue #200: Path 200..."
    current_active_node: "Node 201: Activity 201..."
```

This ensures absolute orthogonal parallelism. Each agent operates exclusively within its own topological coordinate space without semantic contention, preserving the Dao of non-interference (Ziran).

## The Implementation Contract
1. Refactor `kernel/agent_frontier.py` to support read/write operations targeting the `active_agents` matrix based on the currently active `SPAO_PERSONA_ID` environment variable.
2. Maintain backward compatibility gracefully during schema migration.
3. Ensure the active pointer CLI abstractions (`bin/meta active`, etc.) query the correct matrix namespace.
