# WHY-0090: Optimizing node sync for Inner-Loop Velocity

## The Premise
The synchronization phase (`bin/node sync`, backed by `kernel/daemon_node.py:sync_and_clean_node`) is the entrypoint to the SPAO loop. Under the Ziran-aligned principles and Inner-Loop Velocity (SG-0003), this process should be fast and non-obstructive.

## The Problem
Currently, executing `./bin/node sync` takes ~13 seconds. Profiling shows that the CPU time is under 2 seconds, while the remaining 11+ seconds are spent blocked on serial network requests:
1. `git fetch origin --prune`: Network-bound git command (takes 1.5s - 3s).
2. `gh pr list --state open`: GitHub API query for open PRs (takes 1s - 2s).
3. `gh pr list --state merged`: GitHub API query for merged PRs (takes 1s - 2s).
4. `audit_daemon.py`: The metasystem integrity audit is run inline, which performs another remote `get_merged_prs` API call to monitor merged branches (takes 1s - 2s).

This blocking latency violates **Inner-Loop Velocity (SG-0003)** and prevents offline usage.

## Technical Optimization Options

We propose the following multi-tiered optimization strategy:

### Option A: Throttling & Caching of Network Fetches (Default Mode)
Instead of executing network fetches on every single invocation, `node sync` should cache its remote state.
- **Mechanism**: Store the last sync timestamp in a local lock/temp file (e.g., `.locks/last_sync_time`).
- **Policy**: If the last successful sync occurred less than **60 seconds** ago, skip `git fetch` and the GitHub API checks, assuming the state is unchanged.
- **Bypass**: Add a `--force` / `-f` flag to bypass the throttle and force a remote fetch.

### Option B: Local/Offline Mode Flag
Introduce a explicit `--local` / `-l` flag to `./bin/node sync` to completely skip all remote network requests.
- **Behavior**:
  - Skip `git fetch`.
  - Skip `gh pr list --state open` and use local worktrees as the open PR proxy (aligned with `WHY-0089`).
  - Skip remote merged PR queries (only prune local branches that are already merged in the local git repository state).
  - Instruct the audit daemon to run in local-only mode, disabling the remote `pr_merged_monitor`.

### Option C: Audit Daemon Optimization
Update the audit daemon (`drivers/audit_daemon.py`) to:
- Run in `--local` mode when triggered by a local sync, skipping the remote PR merged monitor rule (`pr_merged_monitor`).
- Only run the full remote suite when run by the systemd background cron job.

### Option D: Reactive Event-Driven Synchronization (Chosen Path)
Instead of forcing the Operator to pass manual override flags (Option B) or relying on hardcoded throttling timers (Option A), Option D links network-bound sync operations directly to real-world repository events.
- **Local-by-Default**: `node sync` completes instantly offline by default, skipping remote fetches and PR queries.
- **Event Hook**: The system only performs a remote fetch when a `[NOTIFICATION] Sluice Gate Opened` event is pending in `prompt_backlog.yml` (indicating a PR has been merged on GitHub).
- **Pruning**: Once the PR merge event is processed, the local worktree is cleaned up, the branch is deleted, and the event is consumed.

---

## Chosen Harmonization Path
We select **Option D** (Reactive Event-Driven Synchronization) as it eliminates manual CLI overrides and stateful caches, ensuring zero-latency offline synchronization by default while automatically fetching only when PR merge events dictate a worktree cleanup.

We will:
1. Modify `sync_and_clean_node` in `kernel/daemon_node.py` to check `prompt_backlog.yml` for pending `Sluice Gate Opened` merge events.
2. If no merge events are pending, skip `git fetch` and the GitHub API open PR queries, running the cleanup locally.
3. If a merge event is pending, execute the remote fetch and PR query to prune the worktree, and then mark the prompt as processed.
4. Optimize the audit daemon to disable the remote `pr_merged_monitor` rule when invoked during a local sync.
