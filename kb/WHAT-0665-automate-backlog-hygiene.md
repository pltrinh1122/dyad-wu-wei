# WHAT-0665: Automate Backlog Hygiene via Python Governance Rules

## Functional Requirements
1. **Orphan Detection:** The system must deterministically identify terminal nodes (Activities, Discoveries) that possess the `backlog` label but are not referenced in the `## Meta-Index` of any open parent Path.
2. **Automated Deferral/Cleanup:** Upon detecting an orphaned node, the system must automatically strip the `backlog` label and apply a terminal/deferred status (e.g., `status: deferred`) to prevent it from being fetched by the NBA Scorer.
3. **NBA Scorer Immunity:** `daemon_nba.py` must be hardened to aggressively filter out any unmapped items that do not possess a parent Path when returning Tier 2 Path Switching recommendations. If a node is `unmatched`, it should be explicitly filtered out rather than appended to the end of the backlog queue.
4. **Daemon Integration:** The hygiene logic should be invoked periodically, either during `daemon_nba` execution, `node_lifecycle.py` reflection, or via the `audit_daemon.py`.

## Proposed Architecture
- Modify `kernel/daemon_nba.py`: In the Path Switching tier, strictly filter out `unmatched_items` that are terminal nodes (not paths) rather than appending them to the recommendation list.
- Modify `kernel/daemon_backlog.py`: Introduce a `sweep_orphans()` method that locates all orphaned child nodes and defers them via the GitHub API.
- Create/Modify `kernel/mgr_backlog.py` or `drivers/audit_daemon.py`: Add an `evaluate_orphaned_nodes` rule to trigger the sweep automatically in the background.

## Acceptance Criteria
- Orphaned nodes like Node 33 and 34 no longer cause `bin/status` or `daemon_nba.py` to crash.
- Unmapped terminal nodes are deterministically ignored or deferred without agent intervention.
