# WHY-0095: Group and Align Backlog list with Strategic Goals

## Problem
The previous `backlog-list` CLI output printed a raw, flat list of all backlog issues. This forced the human Operator to pivot between different commands and files to determine (1) which issues are primary Path nodes, (2) how those paths align with active Strategic Goals, and (3) what DAG dependencies exist between paths. This cognitive load violates SG-0004 (efficient communication) and the Wu-wei principle (minimizing total system friction).

## Technical Options

### Option A: Sequential Remote Queries (Falsified)
* **Implementation**: Call the GitHub CLI issue-view command for every open backlog issue to extract its body and dependencies.
* **Falsification**: Sequential network requests on 30+ issues take 15–30 seconds, violating the inner-loop velocity constraint (SG-0003) and slowing the SENSE phase.

### Option B: Local-Only Schema Expansion (Falsified)
* **Implementation**: Store all backlog path descriptions, strategic mappings, and parent-child dependencies directly in `frontier_state.yml` locally.
* **Falsification**: Requires maintaining a duplicate database of GitHub issue properties locally, increasing state synchronization complexity and risk of drift between local metadata and remote issue states.

### Option C: Single-Call Remote Hybrid (Ratified)
* **Implementation**:
  * Execute a single `github-cli-list` call fetching all open issues in JSON format including their numbers, titles, bodies, and labels in under 1 second.
  * Load the local `strategic_intent.yml` file.
  * Filter for issues with the `path` label.
  * Parse dependencies from each path's issue body (searching for `## Depends On`) locally.
  * Group and print paths under their respective active Strategic Goal titles, displaying DAG dependencies inline.
* **Justification**: Combines local-first speed for strategic alignment with a single-request remote fetch for issue bodies, keeping execution under 1 second while completely removing Operator cognitive pivoting load.
