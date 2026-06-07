# WHY-0665: Automate Backlog Hygiene via Python Governance Rules

## Context & Problem Statement
Currently, orphaned child nodes (nodes with the `backlog` and `status: todo` labels but no parent Path linking to them in the Meta-Index) are picked up by `daemon_nba.py` during Tier 2 Path Switching. When `daemon_nba.py` recommends these nodes, the engine attempts to execute `plan-start` on them. However, `plan-start` strictly requires terminal nodes to have a valid parent Path to inherit execution context. Consequently, the system encounters a `[🚫 BLOCKED] Harmonization Failure: Terminal Node #<id> has no parent Path.` error and crashes. This leads to an infinite seizure loop where the daemon repeatedly selects the orphaned node and fails.

Relying on manual LLM agent intervention to sweep the backlog and clean up these orphaned nodes violates the Gateless Autonomous Execution principle. If an agent must manually perform hygiene to keep the engine running, the automation design has failed.

## Strategic Alignment (SG-0001 & SG-0002)
Automating backlog hygiene via deterministic Python rules ensures:
1. **Backlog Dynamics Harmonization (SG-0001):** The backlog remains a pristine queue of valid, executable Paths and Nodes.
2. **Gateless Autonomous Execution (SG-0002):** The NBA daemon can reliably fetch the next node without hitting structurally invalid states that require HITL intervention.

## Architectural Intent
We will implement an automated Python governance rule that sweeps the global backlog, identifies orphaned terminal nodes (missing parent Path lineage), and automatically removes their `backlog` label while transitioning their status to `status: deferred` or closing them. This rule will be integrated into the SPAO execution loop (e.g., within `daemon_backlog.py` or as a standalone `mgr_backlog.py` hook) or directly filtered out within `daemon_nba.py` to ensure orphaned nodes are never considered for path selection.
