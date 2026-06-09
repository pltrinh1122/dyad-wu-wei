# WHAT-1940: Fix System Crash in reflect (--stage none)

## 1. Intent
To resolve the system crash `Command '['git', 'commit', '-m', 'chore(harmonize): complete harmonization for two-tier backlog']' returned non-zero exit status 1` occurring during `bin/node reflect` when using `--stage none`.

## 2. Invariants
- `reflect` mutates `artifacts/frontier_state.*` to advance the system ledger.
- If `--stage none` is used, these modifications were previously unstaged, causing `git commit` to crash.
- **CSI Guard**: Explicitly execute `git add artifacts/frontier_state.*` inside `kernel/node_lifecycle.py` `reflect()` prior to conditional stage evaluation, ensuring the ledger updates are always committed.

## 3. Implementation Steps
1. Modify `kernel/node_lifecycle.py` inside `reflect()` to explicitly stage `artifacts/frontier_state.md`, `artifacts/frontier_state.yml`, and `artifacts/frontier_state.yml.sha256`.
2. Update `tests/test_node_lifecycle.py` to assert the updated `git_client.add` behavior.
3. Validate via `pytest`.
