# Retrospective: Out-of-Cycle Repository Mutation

## The Violation
The Agent attempted to codify a new knowledge primitive (`kb/WHY-0088-interface-as-playbook.md` and modifying `kb/HOW-0000-manifest.md`) directly in the root repository context while operating on a detached HEAD, bypassing the formal **Node-Loop (NL)**. This violates the **Materialization Boundary** and the **Universal Merge Gate (HTIL)** model which requires all repository mutations to go through a dependency-tracked Node, branch, and Pull Request.

## The Root Cause
1.  **Conversational Prompt Trigger**: The Operator suggested that the dynamic playbook insight "feels like an insight that should be codified."
2.  **Lack of Materialization Gating**: The Agent eagerly translated this chat suggestion into direct files without spawning a backlog issue, planning the node contract, checking out a dedicated worktree, and pushing a PR.

## The Epistemic Insight
No knowledge mutation or code change may occur outside of an active Node branch context. Chat requests to codify insights or make edits must be routed through the PML (Pre-Materialization Loop) -> Backlog -> NL pipeline. Direct writes to main or detached HEAD are strictly forbidden.

## The Remediation
1.  Temporarily preserve the new files (`kb/WHY-0088-interface-as-playbook.md` and `HOW-0000` changes) by stashing or copying them.
2.  Reset the root workspace to a completely clean state matching `origin/main`.
3.  Generate a new backlog issue for this alignment/discovery task.
4.  Execute the formal SPAO loop (Plan -> checkout -> apply mutations -> Reflect -> open PR) to commit the changes safely.
