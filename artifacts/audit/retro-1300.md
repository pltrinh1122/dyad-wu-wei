# Epistemic Retrospective: 1300

## 1. The Incident
During the Act phase for Node 1300, the initial test run failed with an `ImportError` because `is_branch_merged_on_github` was removed and replaced with `get_pr_state_by_branch`. Additionally, the lexical guard failed because the word `orchestrator` was found in `kernel/daemon_node.py` when it was modified, which violated the deprecated terminology rule. Finally, the test mocks in `test_node_lifecycle.py` and `test_workspace_init.py` were not updated to expect the new return values (`"MERGED"`, `"CLOSED"`, `"OPEN"`) instead of booleans.

## 2. The Remediation
The lexical guard violation was resolved by replacing `Orchestrator` with `Kernel` in `kernel/daemon_node.py`'s argparse description, adhering to the semantic ledger. The tests were updated to patch the new `get_pr_state_by_branch` function and expect string literals instead of booleans.

## 3. The Insight (WHY-XXXX)
When refactoring legacy helper functions, corresponding test mocks must be proactively updated to match the new return signatures. Additionally, any modifications to existing files will trigger the lexical guard for legacy terminology; these terms must be updated to maintain compliance with `semantic_ledger.yml`.
