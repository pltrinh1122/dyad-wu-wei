# WHY-0054: Metasystem Integrity / Node Sync Latency Optimization

## Context
During the execution of the metasystem integrity check and backlog synchronization (via `./bin/node sync`), the system queries active issues on GitHub. This is part of the Sense phase of our agentic execution loop, ensuring that the local state remains aligned with the remote project backlog.

Historically, this check has suffered from extremely high latency (typically taking upwards of 2 minutes to complete).

## Problem Statement
The latency of `./bin/node sync` acts as a direct bottleneck on the inner-loop execution velocity (violating SG-0003). Profiling reveals that the primary source of latency is `drivers/github_client.py:list_issues_by_label`. 

The function was designed to:
1. List issues matching a label by calling `gh issue list --label <label> --state open --json number,title,url`.
2. For each returned issue, sequentially invoke a separate subprocess `gh issue view <number> --json state` to verify that the state is indeed OPEN.

This O(N) subprocess invocation pattern (where N is the number of open backlog issues) introduces massive network and subprocess creation overhead, taking ~128 seconds for 30 issues. It also increases flakiness due to GitHub rate-limiting and connection resets.

## Proposed Solutions

### Option A: Consolidate to a Single Query (Status Quo Optimization)
Instead of sequentially querying each issue to confirm its state, we can include the `state` field directly in the initial `gh issue list` command's `--json` argument (e.g. `--json number,title,url,state`). 

Because `gh issue list` natively supports returning the state, this consolidates `1 + N` sequential subprocess calls into a single query. The client then simply filters the returned list in memory:
- Old count: `1 + N` network requests.
- New count: `1` network request.

### Option B: Parallelize Queries using Thread Pools
Spawn multiple concurrent threads to query `gh issue view` in parallel. However, this still creates N subprocesses, incurs high CPU context-switching overhead, and exacerbates rate-limiting risks on the GitHub API.

## Architectural Decision
We will implement Option A. Consolidating the retrieval and verification of issue status into a single, unified `gh issue list` query completely eliminates the O(N) sequential loop, achieving true O(1) remote query scaling for this operation. This delivers immediate, massive latency reductions without modifying verification safety or introducing rate-limit vulnerabilities.
