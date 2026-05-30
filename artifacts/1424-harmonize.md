# Harmonize: Redundant Node Closure Discipline

## Context
When an Activity Node is determined to be structurally redundant (i.e. its deliverables were implemented in a prior PR), attempting to follow the strict SPAO workflow generates an empty Pull Request. This introduces cognitive overhead, wastes CI resources, and violates the Wu-wei principle of minimizing friction.

Furthermore, manually closing the GitHub issue without updating the topological ledger (`artifacts/frontier_state.yml`) breaks the `sync` function, causing the `daemon_nba` to continuously recommend a closed issue. Manual intervention via Python scripts triggers a checksum corruption alert (`FRONTIER_INTEGRITY_VIOLATION`), necessitating manual rehashes.

## Architectural Proposal
We must implement a DAO-compliant mechanism for canceling these redundant nodes.

1. **`TerminalNode.cancel`**:
   Extend the `TerminalNode` class in `kernel/node_lifecycle.py` with a `cancel` method. This method will:
   - Close the node's GitHub issue with a specific Metasystem cancellation reason.
   - Utilize `agent_frontier.cancel_active_node` to atomically mark the node as `Cancelled` and clear the active node pointer in the YAML ledger.
   - Uncheck the node's task inside the parent Path's issue body via `BacklogDaemon.check_off_meta_index`.
2. **`cancel_active_node` API**:
   Add this abstraction to `kernel/agent_frontier.py` to handle the atomic ledger manipulation without requiring manual rehashes or PRs.
3. **CLI Invocation**:
   Expose the `cancel` sequence in `kernel/daemon_node.py` via a new `cmd_cancel` handler. This allows the Agent to simply execute:
   ```bash
   ./bin/node cancel <issue_id> <node_name> "<reason>"
   ```
   
This workflow entirely bypasses the PR, Git branch generation, and Observe/Merge phases, natively synchronizing the system state with minimal friction.
