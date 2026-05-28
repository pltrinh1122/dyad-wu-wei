# WHY-0089: Deterministic Zero-Latency State Retrieval

## The Premise
The system status dashboard (`bin/status`) provides a zero-latency system readout to align the Operator and Agent. Under the Ziran-aligned principles, this readout should be deterministic and work completely offline.

## The Problem
Currently, `bin/status` queries the GitHub API (`gh-pr list --state open`) to count open pull requests. This introduces live network dependencies into the status dashboard, which violates:
1. **Inner-Loop Velocity (SG-0003)**: Unnecessary network calls add latency (typically 500ms to 1.5s) to a simple status readout.
2. **Offline Invariance**: If the system is offline, the status check fails or hangs.

## The Alignment (Zero-Latency Local Proxy)
Because our repository enforces strict branch and worktree lifecycles, we do not need to query GitHub to know which PRs are open.

Under our existing architecture:
1. Every active Node is checked out into a dedicated git-worktree located under `.worktrees/` (e.g. `.worktrees/node/<branch_name>`).
2. When a PR is merged on GitHub, the next `Sense` phase (via `sync_and_clean_node`) automatically prunes the merged worktree and deletes the local branch.

Therefore, **the presence of a local worktree is a perfect, zero-latency, offline proxy for an open Pull Request.** 

## Technical Strategy
We will modify `kernel/daemon_status.py` in the next node to:
- Scan the `.worktrees/` directory (specifically `.worktrees/node`, `.worktrees/spao`, and `.worktrees/sdlc`) to identify active worktrees.
- Map each active worktree to its corresponding git-branch.
- Count these active branches as the open/WIP Pull Requests.
- This eliminates the need for live GitHub API requests entirely in the status readout, achieving 100% deterministic zero-latency execution.
