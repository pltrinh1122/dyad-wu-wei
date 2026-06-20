# Harmonize - Node 2204

## Intent
Remediate the globally blocking WIP-N=1 invariant check in `kernel/node_lifecycle.py` to support the Concurrent Factory Floor Pattern, allowing autonomous concurrent evaluation and dispatching of unrelated Paths.

## Changes
1. Modify `kernel/node_lifecycle.py`'s `plan-start` validation logic (around line 290).
2. Update the `open_prs` logic to iterate through active pull requests and check if any PR explicitly conflicts with the *target node* being planned (e.g., checking if the `self.issue_id` exists in the PR's `headRefName` or title).
3. If a PR matches the specific node ID being planned, strictly enforce the WIP-N=1 block to prevent duplicate execution of the same node.
4. If all open PRs belong to *other* nodes, bypass the block to maintain concurrent autonomous throughput.

## Pre-Requisites
- Test suite passes.
- Proper execution workspace checkouts.

## Post-Requisites
- The engine successfully bypasses the WIP-N=1 gate for new nodes when unrelated PRs are open.
- The engine successfully halts and blocks concurrent planning of the *same* node if its PR is open.

## Subagent Delegation
- The `Act` node will implement the conditional PR check in `kernel/node_lifecycle.py` and ensure the local test suite (specifically `test_node_lifecycle.py`) continues to pass.
