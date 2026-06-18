# Harmonize - Path: Concurrent Lock Ledger Materialization (Internal State)

## 1. Intent (WHY)
As we transition from a single Main Agent to a multi-agent concurrent dispatch architecture (Frontier + Sub-Agents), the concept of a monolithic execution lock must be formally deprecated. Currently, residual logic (such as the Orphaned WIP CSI Guard in `kernel/daemon_node.py`) still attempts to validate against a singular, monolithic lock file (`artifacts/frontier_state/lock.json`). Because this file is deprecated and no longer updated, the CSI guard actively falsely detects legitimate concurrent work as orphaned and downgrades their status. To achieve true concurrency, the system must formally materialize the concurrent lock ledger and decouple Execution State from Orchestration State.

## 2. Technical Strategy (WHAT)
- **Axiom Correction:** The Lock-State Axiom must be updated from "WIP=1 globally" to "WIP=1 per persona/agent".
- **Ledger Materialization:** The `active_agents` dictionary within `artifacts/frontier_state.yml` will serve as the formal Execution State Ledger.
- **Guard Evolution:** Update the Orphaned WIP CSI Guard to aggregate all `current_active_node` values across all registered personas in the ledger. If a node is marked `status: in-progress` on GitHub but is not held by *any* agent in the ledger, only then should it be downgraded.
- **Residual Cleanup:** Eradicate all remaining references to the monolithic `lock.json`.

## 3. Scope
- Modify `kernel/daemon_node.py` to refactor the CSI Guard.
- Update `kernel/agent_frontier.py` to expose a helper function (e.g., `get_all_active_nodes()`) that returns a set of all currently locked issue IDs.
