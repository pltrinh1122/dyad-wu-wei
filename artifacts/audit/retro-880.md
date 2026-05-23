# Epistemic Retrospective: Node 880

## The Failure
During the implementation of Activity 880, two distinct execution failures occurred during local test cycles:
1. `ArgumentParser` in `audit_daemon.py` failed with `SystemExit: 2` because it attempted to parse pytest parameters (`sys.argv`) during test execution.
2. `test_sync_and_clean_node_order`, `wip_violation`, and `rom_drift` tests failed because `git_client` and `github_client` local imports inside `sync_and_clean_node` shadowed module-level imports, bypassing pytest patch mocks and triggering real shell execution calls.

## The Epistemic Insight
1. Command-line argument parsers (`argparse`) run inside shared test runners must use `parse_known_args()` rather than `parse_args()` to prevent command-line contamination.
2. Local/inline function imports bypass module-level mock patches. All mock-targeted skills and drivers must be imported at the module level to ensure test isolation is maintained.

## The Remediation
1. Switched `audit_daemon.py` to use `parsed_args, _ = parser.parse_known_args(args)`.
2. Moved the imports of `get_local_worktrees` and backlog queue commands to the module level of `kernel/daemon_node.py` and removed local shadow imports.
3. Restored configuration and backlog states polluted during test failures and staged the corrected files.

## The Synthesis
Unit test isolation requires strict import layout rules and robust CLI parameter parsing to prevent environment leakage. Ensuring module-level visibility for all patchable functions guarantees mock integrity.
