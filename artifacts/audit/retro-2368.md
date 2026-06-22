# Retro 2368: Reflect Phase Failure

## Context
During the Act phase of Node #2368, the agent manually executed `git commit` to save work before running `./bin/node reflect 2368`.

## Failure Trigger
The `daemon_node.py reflect` script executes `git commit` as part of its pipeline. Because the working tree was already clean (the commit was already made manually), the `git commit` command inside `reflect` failed with exit code 1 (`nothing to commit, working tree clean`). This caused a FlowTransaction failure, rolling back the reflect phase.

## Remediation
Following the Rollback Invariant, the remote branch was deleted (if it existed), the local branch was reset to `origin/main` to remove the manual commit, and the modified files were restored to the working directory without a manual commit. The reflection phase will now be re-executed, allowing the system to handle the commit natively.

## Lesson
The Agent MUST NOT manually commit changes before calling `reflect`. The `reflect` phase encapsulates the commit logic autonomously.
