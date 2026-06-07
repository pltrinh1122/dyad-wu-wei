# WHAT-1804: Checkout Crash Graceful Validation Plan

## Context
Node #1803 harmonized the intent that a malformed branch name during `checkout` must be treated as a validation boundary rather than an unhandled system crash. This prevents the top-level exception handler from invoking the automated bug intake process.

## Implementation Plan
1. **Target Module**: `kernel/daemon_node.py`
2. **Target Function**: `cmd_checkout(args)`
3. **Change**:
   - Wrap the call to `checkout_node(args.issue_id, args.branch_name)` in a `try...except ValueError` block.
   - On exception, log the error message using `sys.stderr.write()` or `print(..., file=sys.stderr)`.
   - Exit gracefully using `sys.exit(2)`.

## Test Plan
- Update `tests/test_daemon_node.py` or equivalent test suite to cover the validation failure path.
- Assert that `cmd_checkout` exits with code 2 when a `ValueError` is raised by `checkout_node` due to an invalid branch name.
