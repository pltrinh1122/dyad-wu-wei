# WHAT-2184: DAG Execution and NBA Remediation

## 1. Intent
To ensure frictionless execution of the autonomous SPAO pipeline, we must codify invariants that prevent manual interventions during DAG evaluation and node aborts.

## 2. Abort Lifecycle Hygiene
When `bin/node abort` is executed, the system MUST:
1. Revert the GitHub issue's physical label to `status: todo` (not `open`, which is obsolete).
2. Explicitly append the `backlog` classification label to ensure the issue is eligible for future NBA intake.

## 3. Terminal Reflect Invariant
When calculating ready nodes within a Path (`drivers/gh_graph_skill.py`):
1. A node classified as `Reflect` (e.g. title contains `Reflect`) MUST NOT be returned as ready unless it is the **only** incomplete node remaining in the `Meta-Index`.
2. This eliminates the need to continuously rewrite `[Depends: XXX]` pointers when injecting new `Act` nodes sequentially via `bin/backlog`.

## 4. Universal Topological Pass
The NBA evaluation engine (`kernel/daemon_nba.py`) MUST:
1. Apply the topological DAG sort (`get_ready_nodes`) to **all** open paths, including dynamically generated BUG paths, before resorting to fallback arrays.
2. Ensure that Path container nodes (issues with the prefix `Path:`) are explicitly stripped from the `recommendations` output pool, as they are non-terminal and cannot be `plan-start`ed.
