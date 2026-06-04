## Goal
Implement a metadata guard to verify executable bits for bin/* scripts.

## Execution
- Created `tests/test_bin_executable.py` to enforce that all files in the `bin/` directory have their executable (`+x`) bits set.
- Validated test suite passes.
