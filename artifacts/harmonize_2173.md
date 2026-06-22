# Harmonize - Node 2173: System Crash in checkout

## Root Cause Analysis
During an automated path execution, if a previous failure occurred (e.g., `reflect` failed and rolled back), the git branch or the worktree path might be left behind locally. 
When the system eventually re-attempts to execute the node, it calls `node.checkout()`, which in turn executes `git worktree add -b <branch> <path> origin/main`.
If the branch or worktree directory already exists, `git` returns a non-zero exit code (255).
Currently, this native `subprocess.CalledProcessError` bubbles up completely unhandled, crashing the daemon and forcing an unnecessary Bug Intake loop.

## Proposed Alignment
The `checkout` phase is a structural part of the `FlowTransaction`. 
Just as `reflect` handles known local blockages by raising a structured `ReflectionBlockedError` (so the transaction can gracefully roll back and mark the node `[🚫 BLOCKED]`), the `checkout` phase must handle git worktree creation failures.

We should align on:
1. **Graceful Exception Mapping:** Catch `subprocess.CalledProcessError` inside `kernel/node_lifecycle.py:checkout` when calling `git_client.worktree_add`.
2. **Structured Abort:** Raise a structured `CheckoutBlockedError` (which needs to be defined in `kernel/node_lifecycle.py` or a dedicated exceptions module).
3. **Transaction Safety:** Allow `FlowTransaction` to catch `CheckoutBlockedError`, abort the node execution gracefully, and label it `[🚫 BLOCKED]` in the backlog instead of crashing the system.

This ensures the daemon remains robust against dirty local git states.
