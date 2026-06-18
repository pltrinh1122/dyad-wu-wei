---
type: WHAT
path_id: 2102
title: Concurrent DAG Evaluation (The Scoring Alg)
---

# Scope
Evolve the Next-Best-Action (NBA) logic in `kernel/daemon_nba.py` to explicitly separate Available for Dispatch nodes from Currently Locked by Workers nodes, ensuring concurrent safety during multi-agent orchestration.

# Requirements
1. **Identify Locked Nodes**: The `evaluate` method MUST read `artifacts/frontier_state.yml` to collect all `current_active_node` values from the `active_agents` mapping.
2. **Path Continuation Filtering**: Any node ID present in the `locked_node_ids` set MUST NOT be recommended in the `path_continuation` phase.
3. **Path Switching Filtering**: Any node ID present in the `locked_node_ids` set MUST NOT be recommended in the `path_switching` phase.
4. **Resiliency**: The engine must not crash if the `frontier_state.yml` is temporarily malformed.
5. **No Double-Dispatch**: Prevents the kernel_daemon from dispatching the same open node to multiple sub-agents.
