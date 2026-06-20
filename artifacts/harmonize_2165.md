# Harmonize - Node 2165: Re-architecture of Path Container State Preservation

## Root Cause Analysis (RCA)
**The Orphaned Path Phenomenon**
Currently, the Orchestrator's SENSE loop and `nba.evaluate` rely on markdown checkbox parsing within the body of a "Path" container issue (`[ ]` vs `[x]`) to determine the Path's state and next best child node. 

1. **Fragile State Storage:** The execution state of a Path is redundantly stored as unstructured text within the parent issue's `Meta-Index` block. 
2. **Synchronization Gaps:** The checkboxes are only checked off successfully if `bin/node reflect` runs to completion and successfully calls `daemon_backlog.check_off_meta_index()`. 
3. **Out-of-Band Discrepancy:** If a child node is closed manually (`gh issue close`), aborted, canceled, or updated via out-of-band mechanics, the parent Path's checkboxes remain unchecked. The NBA scorer (`gh_graph_skill.get_next_nodes`) therefore continuously evaluates the Path as having pending nodes, preventing `node_lifecycle.py` from auto-closing the Path, resulting in perpetual orphans.

## Proposed Architectural Shift
We must decouple the Orchestrator from the fragility of markdown checkbox parsing and rely on a definitive, verifiable State Machine mechanism.

**Option 1: GitHub State as the Source of Truth (Remote Invariant)**
- **Mechanism**: The NBA evaluator (`gh_graph_skill.get_next_nodes` and `daemon_nba.py`) will parse the `Meta-Index` only to discover the Issue IDs of the child nodes. It will then dynamically query the GitHub API to check the actual `state` (OPEN vs CLOSED) of each child node. 
- **Benefits**: Completely immune to out-of-band closures. If a node is closed for any reason, the system correctly recognizes it as finished. 
- **Auto-Closure**: If all extracted child IDs report as `CLOSED`, the parent Path is automatically closed by the SENSE phase.

**Option 2: Multidimensional Lock Ledger (Local State Invariant)**
- **Mechanism**: Expand on the existing `frontier_state.yml` architecture to maintain a definitive, concurrent state machine for all active Paths and their sub-node transitions. 
- **Benefits**: Reduces GitHub API calls, operates in a true lock-free concurrent manner, and formally splits Orchestration State from Execution State.

**Recommended Alignment**
We should proceed with **Option 1 (GitHub State as Source of Truth)** as the immediate tactical fix for the NBA evaluator to stop the orphan bleed, coupled with an update to `daemon_nba.py` and `gh_graph_skill.py`. This ensures the "Dark Substrate" remains robust regardless of how issues are closed.

## Changes
- Update `gh_graph_skill.get_next_nodes()` or `daemon_nba.py` to filter child nodes based on their remote `state: open/closed` rather than the regex `[ ]` parsing.
- Update `node_lifecycle.py` to auto-close the Path if `nba.evaluate` returns an empty array for a Path because all child nodes are `state: closed`.
