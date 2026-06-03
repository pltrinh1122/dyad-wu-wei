# WHAT-1644: Reflect Worktree Guard

## Execution Context
The Agent must not execute the `reflect` command from within a worktree directory. Doing so causes `path_resolver` and `os.getcwd()` to evaluate the worktree as the repository root, leading to double-nested directory evaluations that crash underlying system subprocesses.

## Technical Specification
1. **Target**: `kernel/daemon_node.py` inside the `cmd_reflect(args)` function.
2. **Implementation**: Add an explicit check against `os.getcwd()`.
   ```python
   def cmd_reflect(args):
       import os
       import sys
       if ".worktrees" in os.path.abspath(os.getcwd()).split(os.sep):
           sys.exit("[🚫 BLOCKED] Reflection Blocked: You must run the reflect command exclusively from the repository root directory, not from within the active worktree.")
   ```
3. **Outcome**: The command gracefully rejects invalid execution contexts before any destructive `git` operations or file manipulations are attempted, replacing an obscure `FileNotFoundError` system crash with a clear invariant enforcement.
