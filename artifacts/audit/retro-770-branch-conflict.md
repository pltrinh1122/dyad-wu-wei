# Retrospective: PR Conflict Resolution Violation

## Violation
During the execution of Node 770, the Agent pushed a branch (`node/770-autonomous-learning-loop`) and submitted a Pull Request that contained unresolved merge conflicts in the `artifacts/frontier_state.*` tracking files. This shifted the cognitive burden of conflict resolution onto the Operator, violating **SG-0002 (Containment & Delegation)**.

## Correction
The Operator flagged the PR as having unresolved conflicts via chat. 

## Codified Insight
In accordance with the Autonomous Learning Loop (**WHY-0082**), the Agent immediately transitioned into Epistemic Reflection. We identified that the lack of an automated conflict-verification step prior to `reflect` enables this failure mode. We have codified the rule that Agents must locally resolve all conflicts in **WHY-0083**.

## Action Items
1. Created `kb/WHY-0083-pr-conflict-resolution.md`.
2. Resolved the active merge conflicts in Node 770's worktree manually and force-pushed the corrected branch.
3. Spawned an Activity in the backlog to implement a programmatic pre-reflection guardrail that fails-closed if conflicts are detected.
