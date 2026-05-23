# WHAT-0090: Reactive Event-Driven Synchronization Specification

This document defines the formal specification for **Option D (Reactive Event-Driven Synchronization)** to refine `bin/node sync` performance.

---

## 1. Local-by-Default Invariant
By default, the SENSE phase sync process must operate entirely offline with zero network latency.
- `sync_and_clean_node` in `kernel/daemon_node.py` must skip the remote git-fetch call and remote GitHub API queries for open PRs.
- Local worktrees (detected via `.worktrees/`) serve as the authoritative proxy for open PRs, preventing the need for remote queries.

---

## 2. Event-Driven Remote Trigger
The sync process will dynamically trigger a remote fetch and worktree pruning only when a real-world merge event dictates it:
- SENSE reads `artifacts/prompt_backlog.yml` at start.
- If a prompt is found with the text prefix `[NOTIFICATION] Sluice Gate Opened: PR for Node` and status is `pending`, the sync daemon transitions to **Remote Mode**.
- In Remote Mode, the system:
  1. Executes the git-fetch operation to retrieve remote main branch updates.
  2. Queries GitHub for the merged PR branches.
  3. Prunes the matched worktree and deletes the local branch.
  4. Marks the `Sluice Gate Opened` notification prompt as processed and consumes it.

---

## 3. Local Audit Execution
To prevent inline audit latency:
- The audit daemon (`drivers/audit_daemon.py`) must support a `--local` CLI switch.
- When invoked as part of a local-by-default sync, `daemon_node.py` will pass the `--local` flag to `audit_daemon.py`.
- The audit daemon will bypass the network-bound `pr_merged_monitor` rule, completing the integrity audit instantly.
- The full remote `pr_merged_monitor` suite remains active when triggered by the systemd background cron job.
