# Epistemic Retrospective: Node 1485

**Node Reference:** Node 1485 (Activity: Falsify and remediate dz-cil survivors)

## Execution Failure
During the Act phase, a test suite failure (`StateCorruptionError: Frontier state checksum mismatch!`) occurred. 

## Root Cause
A Python script was executed to perform a workspace-wide find-and-replace of `dz-cil` to `dyad-wu-wei`. It attempted to ignore `.git` as a directory, but in a worktree, `.git` is a file. The script thus inadvertently mutated the worktree's `.git` gitdir reference, breaking `git status`. It also mutated `artifacts/frontier_state.yml` causing a checksum mismatch.

## Remediation
The `.git` gitdir file was manually restored to `dz-cil`. The `artifacts/frontier_state.yml` was successfully rehashed using `./bin/meta rehash`. Tests then passed cleanly.

## Lesson Learned
When doing brute-force string replacement across a workspace, always strictly verify file types (e.g. `os.path.isdir`) and do not assume `.git` is a directory in a worktree context. Also, changes to checksum-protected files must be explicitly rehashed.
