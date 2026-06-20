# WHAT-2166: Re-architecture of Path Container State Preservation

## Context
Path nodes act as 'container' nodes, maintaining a markdown DAG of their children nodes. Previously, the DAG parser (`gh_graph_skill.py`) relied exclusively on regex parsing of markdown checkboxes (e.g., `[x]` vs `[ ]`) to determine if a child node was completed. This created a fragile architecture where PR merges closed child issues but did not automatically check off the markdown checkboxes in the parent Path issue body, leading to "orphaned" Path nodes and execution seizures.

## Architectural Change
We shift the source of truth for node completion from the markdown text to the actual GitHub Issue state.
1. `gh_graph_skill.get_ready_nodes()` now intercepts the parsed markdown state.
2. For any node marked as incomplete (`[ ]`) in the markdown, the system performs a direct GitHub API query (`github_client.get_issue_details`).
3. If the actual GitHub Issue state is `CLOSED`, the DAG evaluator overrides the markdown state, marking the node as completed.

## Invariants Maintained
- The markdown Meta-Index remains the structural source of truth (defining the nodes and dependencies).
- The GitHub API becomes the stateful source of truth for completion, eliminating synchronization friction.
- This directly satisfies the Operator's requirement to wrap `gh` with CSI-style API verification and remediate orphaned Path states without manual hygiene sweeps.
