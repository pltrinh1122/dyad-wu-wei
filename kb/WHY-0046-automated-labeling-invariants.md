# WHY-0046: Automated Labeling Invariants — Alignment

## Rationale
Manual updates to GitHub issue labels during node transitions are error-prone and lead to metadata drift (such as closed issues retaining active status labels or paths missing the `path` label). 

To ensure complete metadata integrity and consistency with local ledger files (`frontier_state.yml` and `frontier_state.md`), labeling invariants must be enforced programmatically by the orchestrator commands.

## Solution Design
1. **Unified Status Management**: Introduce automated status label transition logic within `kernel/daemon_node.py` and `kernel/node_lifecycle.py`.
2. **Hook Execution**: During transitions:
   - `plan_start`: Apply the `status: in-progress` label.
   - `reflect`: Close the issue and remove all `status:` prefix labels.
3. **Registration Guard**: When creating new nodes via `BacklogManager`, apply standard `backlog` or `path` labels automatically.
