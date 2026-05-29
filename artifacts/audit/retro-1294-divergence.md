# Epistemic Retrospective: 1294-divergence

## 1. The Incident
The system became halted because the offline SENSE phase `sync_and_clean_node` raised a WIP-N=1 invariant violation due to the presence of the local worktree `.worktrees/node/1294-fix-mock-accrual-tests`. The Operator had already closed the PR externally.

## 2. The Divergence
The `bin/status` command relies purely on the physical existence of a local `.worktrees/node/<id>` directory to declare "Open PRs", rather than querying the remote GitHub state. 
Simultaneously, `sync_and_clean_node` running in default offline mode refuses to check GitHub to verify if the corresponding PR is actually closed/merged, opting instead to throw a hard halt and forcing manual Operator intervention.

## 3. The Epistemic Insight
Offline-by-default execution (SG-0003) is meant to preserve velocity by eliminating network I/O, but it becomes an anti-pattern when it forces manual Operator intervention (violating SG-0002). When an active local worktree is detected during the SENSE phase, the system MUST selectively fetch the remote status of that specific Node's PR before raising a blocking WIP-N=1 violation.

## 4. Remediation
1. The blocking worktree `.worktrees/node/1294-fix-mock-accrual-tests` was manually deleted to immediately unblock the SENSE loop.
2. A prompt was added to the queue to formally remediate `sync_and_clean_node` and `bin/status` to accurately fetch and reflect remote PR states for active worktrees, thus preventing recurrence.
