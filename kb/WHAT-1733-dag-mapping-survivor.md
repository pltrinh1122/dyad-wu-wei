# WHAT-1733: DAG Mapping Survivor (`bin/backlog map`)

## Objective
Implement a mechanism that explicitly visualizes the backlog DAG, rooting open Paths and Activities against the overarching Telos (the Summit). This formalizes the "Survivor" identified in WHY-1731.

## Architecture

1. **Target Subsystem**: `kernel/daemon_backlog.py`
2. **New Sub-command**: `map`
   - Invocation: `./bin/backlog map`

3. **Data Retrieval Strategy**:
   - Query all open issues in the repository (`github_client.list_all_open_issues()`).
   - Extract titles, labels, and issue bodies.

4. **Parsing Strategy**:
   - Parse parent-child relationships (e.g., Activity Nodes parsed from Path Meta-Index bodies).
   - Parse peer dependencies (`Depends On: <ID>` from Activity bodies).

5. **Synthesis Strategy**:
   - Create a Root Node `Summit` (Telos of Wu-wei).
   - Link all open Path issues to the `Summit`.
   - Link all Activity/Discovery issues to their parent Path issues.
   - Inject dotted-line lateral links for `Depends On` relationships.
   - Output the synthesized DAG as a Mermaid.js Markdown block to `STDOUT`.

6. **Execution Integration**:
   - The user/Agent can pipe this output to an artifact (`artifacts/summit_map.md`) or directly inspect it in the CLI to orient themselves within the global topological landscape.
