# Retro Node 606: Probe 606: Align - Exclude Locked Nodes from NBA Path Continuation

## Failure Mode
The `bin/node reflect` command failed with a non-zero exit status during the commit phase (`nothing to commit, working tree clean`).

## Root Cause
An "Align" Probe strictly creates architectural artifacts (e.g., `implementation_plan.md`) which exist outside the git repository (or in an ignored directory). Because no tracked source files were modified, `git commit` failed when attempting to reflect the node.

## Remediation / Lesson Learned
When reflecting an "Align" Probe or any Node that does not mutate git-tracked files, the `--stage none` parameter must be explicitly passed to `bin/node reflect` to bypass the git commit enforcement.

## Policy Update
No global policy update is required. This is an operational procedure correction for the agent executing the SPAO loop.
