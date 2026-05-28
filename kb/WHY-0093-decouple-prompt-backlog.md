# WHY-0093: Decouple Prompt Backlog from Git Tracking

## Problem Statement
The operator's asynchronous instructions are queued locally inside `artifacts/prompt_backlog.yml` while executing. However, because this file is currently tracked in the Git repository:
1. Running destructive git operations (such as `git-restore .` or `git-checkout`) to clear local working tree conflicts resets `artifacts/prompt_backlog.yml` to the remote branch state (`prompts: []`), permanently erasing the operator's queued prompts.
2. Concurrent agent execution sessions on separate branches will inevitably lead to merge conflicts in `artifacts/prompt_backlog.yml`.
3. Routine prompt queue changes pollute the git history.

## Harmonization Analysis
To resolve this state collision, we evaluated the following technical alternatives:

1. **Option A: Backup and Restore in Git Wrapper Shells**
   - *Pros*: Keeps the file tracked.
   - *Cons*: Highly fragile; requires wrapping every raw git command to copy and restore prompt backlog state. Does not solve branch merge conflicts.

2. **Option B: Untrack and Ignore in Git (.gitignore)**
   - *Pros*: Eliminates repository conflicts entirely. Prompt backlog becomes a purely local, persistent state file that is completely immune to git switches, checkout resets, or restores.
   - *Cons*: The file must be initialized cleanly on new checkouts.

## Alignment Rationale
We align on **Option B**. Storing a transient session queue (the prompt backlog) as a tracked repository file violates the principle of separation of concerns. Decoupling the file from Git tracking makes it a persistent local state file, safeguarding operator instructions.

## Implementation Blueprint
1. Remove `artifacts/prompt_backlog.yml` from tracking:
   - Execute `git-rm --cached artifacts/prompt_backlog.yml`.
2. Add `artifacts/prompt_backlog.yml` to the root `.gitignore` file.
3. Ensure the prompt daemon initializes a default empty queue file if it does not exist during status checks or sync actions.
