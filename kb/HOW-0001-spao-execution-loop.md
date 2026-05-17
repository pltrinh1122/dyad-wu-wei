# HOW-0001: The SPAO + HITL Execution Loop

This document contains the strict, deterministic instructions (The "How") for operating the Meta-Orchestrator loop.

## The Execution Loop Steps
The master objective is decomposed into discrete topological **Nodes**. For each Node, the Agent **must** execute the following loop in exact order:

1. **Sense (Pre-Condition):** 
   - Execute the shell script: `./bin/sync-clean` to fetch `main`, safely delete old merged branches, and **surface any pending backlog items**.
   - Read `artifacts/frontier_state.md` and the cloud-hosted Path Meta-Index (GH Issue).
   - Validate that the feedforward invariants from the previous node are met.
   - If backlog items are surfaced, pull the highest-priority item as the next Node (unless the Operator specifies otherwise).

1. **Plan (Contract Formulation):** 
   - Execute the shell script: `./bin/node plan "ISSUE_ID" "Body content..."` to lock the Node Contract into the existing **Backlog Issue** and automatically prepend the Node ID to the GitHub Issue title.
   - **Meta-Rule Invariant:** Node Issues MUST be pulled from the backlog. It is mathematically forbidden to generate a new issue out of thin air during the Plan phase. The Node ID is mathematically isomorphic to the GitHub Issue ID.
   - **Template Invariant:** The Agent must NEVER generate inline markdown strings for GitHub Issues. All issue bodies (Backlog and Node Contracts) MUST be rendered using strict, Operator-editable templates located in `kb/templates/`.
   - Mutate the body of the **Path Issue** to link to the newly active Node Issue via `./bin/meta link "Node X: Title" "ISSUE_ID"`.
   - *Do not execute codebase mutations until the Node Issue is explicitly locked.*

3. **Act (Execution):** 
   - Execute codebase generation, tool invocations, and artifact mutations required by the Scope.
   - **TDD Invariant:** You MUST use `./bin/run-tests` for all local testing. Raw bash `pytest` is strictly forbidden.

4. **Observe (HITL Pause):** 
   - The Agent halts execution.
   - The Operator executes the local environment, evaluates the state, and provides Human-In-The-Loop feedback.
   - The Agent must formally log any constraints or feedback provided by the Operator as a comment on the Node Issue.

5. **Reflect & Advance (Post-Condition):** 
   - Execute the shell script: `./bin/reflect-node "ISSUE_ID" "Node X: Title" "Learnings..." "['[x] Invariant']" "commit message" "node/XX-kebab-case" "PR Title"
   - This atomic skill will rigorously enforce branch naming, update `artifacts/frontier_state.md`, push the branch, and automatically open a Pull Request.
   - Mutate the **Path Issue** body to check off the completed node.
   - **HARD HITL BLOCK:** The Agent must absolutely halt and wait for the Operator to review and merge the PR before proceeding to the next node.

## Executing the Formal Bootstrap Audit
Before a newly bootstrapped repository can transition into active "Operations," it must pass an audit.
1. The Agent must fetch the `HOW-0002-bootstrap-audit-template.md` from the `agent-antigravity` meta-repository.
2. The Agent opens a new Node Issue using this template.
3. The Agent performs the compliance checks against the codebase and checks off the boxes in the issue body.
4. The Agent pauses (Observe phase) for a final Operator HITL sign-off before closing the audit ledger.
