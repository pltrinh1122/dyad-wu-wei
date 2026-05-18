# WHY-0002: GitHub API Eventual Consistency on Issue State

## 1. The Phenomenon
During the `Sense` phase, immediately after merging a Pull Request that automatically resolves an issue (via the `Resolves #XYZ` keyword), the `bin/node sync` orchestrator may momentarily present the recently closed issue in the pending backlog.

## 2. Root Cause Analysis
The anomaly stems from GitHub's fundamental architectural separation between its strongly-consistent relational datastore (the Issues API) and its eventually-consistent ElasticSearch index (the Search API). 

The Antigravity system invokes `gh issue list --label backlog --state open`. Under the hood, the GitHub CLI proxies this request to the GitHub Search API (`/search/issues`). When a PR is merged, the core datastore instantly transitions the issue state to `closed`. However, propagating this state mutation to the Search API's distributed inverted index incurs an arbitrary synchronization latency (typically 2-10 seconds, but subject to global load). 

Consequently, if `bin/node sync` is executed within this latency window, the Search API will serve stale data, incorrectly returning the issue as `open`.

## 3. The Mitigation Strategy (Activity Generation)
Because the `gh issue view <id>` command interrogates the strongly-consistent Issues API directly, we must decouple the *discovery* of issues from the *verification* of their state.

To mathematically eliminate this ghost-state collision, we must:
1. Continue utilizing `gh issue list` (Search API) for initial label-based discovery.
2. For each discovered issue, forcefully invoke `gh issue view <id> --json state` (Issues API) to definitively verify its state.
3. Only surface the issue to the agent loop if the strongly-consistent API confirms it is genuinely `OPEN`.

*This architectural invariant has been formally queued for implementation in a subsequent Activity Node to preserve the Probe isolation invariant.*
