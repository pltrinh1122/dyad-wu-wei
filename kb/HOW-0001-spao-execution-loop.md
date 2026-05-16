# HOW-0001: The SPAO + HITL Execution Loop

This document contains the strict, deterministic instructions (The "How") for operating the Meta-Orchestrator loop.

## The Execution Loop Steps
The master objective is decomposed into discrete topological **Nodes**. For each Node, the Agent **must** execute the following loop in exact order:

1. **Sense (Pre-Condition):** 
   - Read `artifacts/frontier_state.md` and the cloud-hosted Epic Meta-Index (GH Issue).
   - Validate that the feedforward invariants from the previous node are met.

2. **Plan (Contract Formulation):** 
   - Execute a `gh issue create` command to create a **Node Issue** defining the exact Scope and Acceptance Criteria.
   - Mutate the body of the **Epic Issue** to link to the newly active Node Issue.
   - *Do not execute codebase mutations until the Node Issue is created.*

3. **Act (Execution):** 
   - Execute codebase generation, tool invocations, and artifact mutations required by the Scope.

4. **Observe (HITL Pause):** 
   - The Agent halts execution.
   - The Operator executes the local environment, evaluates the state, and provides Human-In-The-Loop feedback.
   - The Agent must formally log any constraints or feedback provided by the Operator as a comment on the Node Issue.

5. **Reflect & Advance (Post-Condition):** 
   - Execute `gh issue close` to seal the Node Issue, rendering it an immutable transaction log.
   - Mutate the **Epic Issue** body to check off the completed node.
   - Synthesize learnings and write them to `artifacts/frontier_state.md`.
   - Advance the active topological node pointer to await the next objective.

## Executing the Formal Bootstrap Audit
Before a newly bootstrapped repository can transition into active "Operations," it must pass an audit.
1. The Agent must fetch the `HOW-0002-bootstrap-audit-template.md` from the `agent-antigravity` meta-repository.
2. The Agent opens a new Node Issue using this template.
3. The Agent performs the compliance checks against the codebase and checks off the boxes in the issue body.
4. The Agent pauses (Observe phase) for a final Operator HITL sign-off before closing the audit ledger.
