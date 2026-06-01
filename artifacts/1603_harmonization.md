# 1603 Harmonization: Falsify PR and Node Conflation & NBA Sync Recovery

## Philosophical Intent
Historically, the Agent conflated PR IDs with Node IDs because GitHub issues and pull requests share the same global ID sequence. When the system reported `Cannot plan node #Y because there are open pull requests: [X]`, the Agent would incorrectly interpret `X` as a Node ID, rather than a Pull Request ID.

During this discovery phase, we discovered a compounding failure:
GitHub recently started outputting a GraphQL deprecation warning to `stderr` (`GraphQL: Projects (classic) is being deprecated`) for all `gh issue view` and `gh pr view` commands, and returning a non-zero exit code (1). This caused the system's `github_client.py` to raise `subprocess.CalledProcessError` on any operation verifying node state, which fatally disrupted the NBA extraction in `kernel/daemon_nba.py`. The `daemon_nba.py` would silently catch this exception and fall back to scanning a corrupted local `frontier_state.md`, causing it to surface ghost tasks like `Node 31: Future Work Item`.

## Technical Harmonization
1. **Conflation Fix (Applied in Activity 1606)**:
   - Falsified the PR/Node equivalency thesis by ensuring the `WIP-N=1` invariants explicitly emit the `headRefName` alongside the integer PR ID.
   - Example: `PR #1607 (branch: node/1606-falsify-pr-node-conflation)`.

2. **GitHub Client Robustness**:
   - Modified `drivers/github_client.py::_run_gh()` to intercept `check=True`.
   - If a non-zero exit code is encountered, but the command requested JSON output (`--json`) and valid JSON is parsed from `stdout` (after stripping warnings), the error is suppressed.
   - This hardens the `gh` abstraction layer against non-fatal deprecation warnings and restores NBA autonomous handoff stability.
