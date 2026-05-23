# Node 818 Post-Mortem

## Failure Trigger
During the execution of Node 818 (Injecting WIP-N=1 Hard Gate Safeguard), `spao test` failed in `test_node_lifecycle.py` and `test_daemon_node.py` with:
`Exception: WIP-N=1 Invariant Violation: Cannot plan node #157 because there are open pull requests: []`

## Root Cause
The newly implemented safeguard in `node_lifecycle.py` checks `if open_prs:`.
In the test suite, `github_client` was mocked as an overarching `MagicMock`. Because `get_open_prs` was not explicitly given a `return_value = []` in the setup blocks for `test_plan_start_node` and `test_checkout_node`, it returned a fresh `MagicMock` object. In Python, `MagicMock` objects natively evaluate to `True`, triggering the safeguard exception even though the conceptual state was meant to have 0 open PRs.

## Corrective Action
- Explicitly defined `mock_gh.get_open_prs.return_value = []` in the test setup blocks for all relevant tests within `test_daemon_node.py` that invoke `plan_start` or `checkout`.
- Re-ran the test suite ensuring a full 100% pass rate.
