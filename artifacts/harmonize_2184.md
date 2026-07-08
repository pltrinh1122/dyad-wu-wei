# Harmonize - Remediate DAG Execution and NBA Fallback Invariants

## Context & Synthesis
During the execution of recent Paths (e.g., Path 2168, Path 2172), the Operator experienced several architectural bottlenecks requiring manual intervention. We have cataloged these interventions into a unified R&D node to address their root causes and implement frictionless "dark" substrate invariants.

### 1. The Abort / Orphan State Bug
**Symptom**: When `bin/node abort` is used, the targeted node's status is reset, but it gets stranded and is no longer picked up by the NBA engine.
**Root Cause**: 
`kernel/node_lifecycle.py` uses `self.set_status("open")`, which fails because the physical mapping for "open" was replaced by `"clarify"` in `node.yml`. Furthermore, when a node is locked via `plan-start`, it is purged from the Tier-2 `global_backlog.yml` cache and its `backlog` label is stripped from GitHub. When `abort` is called, it fails to re-apply the `backlog` classification label, leaving the node without the intake mechanism needed for the NBA engine to re-evaluate it.

### 2. The Backlog Appending Dependency Bug (DAG Rewiring)
**Symptom**: When `bin/backlog new activity` is executed to add an `Act` node, the `Reflect` node's `[Depends: <Plan-ID>]` string in the parent Path's Meta-Index is not updated. This causes `gh_graph_skill` to treat both `Act` and `Reflect` as ready the moment `Plan` is completed. Because `Reflect` has an older issue ID, the naive numerical sort prioritizes it over `Act`.
**Root Cause**:
`daemon_backlog.py` naively prepends new node lines into the `Meta-Index` list using simple regex text replacement without comprehending the topological DAG.
**Resolution Intent**: Instead of building complex string parsing to constantly rewrite `[Depends: X]` pointers, `gh_graph_skill.py` should enforce a structural invariant: a node containing "Reflect" in its title is structurally bound as the terminal node of its Path, meaning it cannot be evaluated as "ready" until all other child nodes within the same Meta-Index are marked as completed. This eliminates the fragility of string-based pointer management.

### 3. The Unmatched / Fallback NBA Topological Failure
**Symptom**: Bug Paths (which are dynamically ingested and not part of the static `strategic_intent.yml`) fall through to the "unmatched_items" fallback logic in `daemon_nba.py`. The fallback logic simply sorts the open nodes by issue ID and ignores their DAG dependencies entirely.
**Root Cause**:
`daemon_nba.py` bypasses `gh_graph_skill.get_next_nodes` for issues that aren't mapped to prioritized Paths. It also erroneously evaluates Path container nodes (which are just grouping mechanisms) as executable nodes, attempting to lock them.
**Resolution Intent**: `daemon_nba.py` must apply topological DAG sorting (`get_next_nodes`) to **all** open paths, regardless of whether they exist in `strategic_intent.yml` or the `global_backlog` fallback. Additionally, Path container issues must be strictly filtered out of the final recommendation pool—they are non-terminal and cannot be `plan-start`ed directly.

## Feedforward Invariants
- `kernel/node_lifecycle.py`
- `kernel/daemon_backlog.py`
- `kernel/daemon_nba.py`
- `drivers/gh_graph_skill.py`
