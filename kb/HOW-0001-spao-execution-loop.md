# HOW-0001: The SPAOR + HITL Execution Loop

This document contains the strict, deterministic instructions (The "How") for operating the Frontier Agent loop.

## The Execution Loop Steps
The master objective is decomposed into discrete topological **Nodes**. For each Node, the Agent **must** execute the following loop in exact order:

1. **Sense (Pre-Condition):** 
   - Execute the shell script: `./bin/node sync` to fetch `main`, safely delete old merged branches, and **surface any pending backlog items**.
   - Read `artifacts/frontier_state.md` and the cloud-hosted Path Meta-Index (gh-issue).
   - Validate that the feedforward invariants from the previous node are met.
   - **The WIP Invariant:** The system operates strictly on a single node execution thread (`WIP-N=1` and `WIP-P=1`). Node branches MUST strictly conform to the format `node/<id>-<kebab-case>` (e.g. `node/906-harmonize-backlog-cli`).
   - **Path Initialization Invariant:** When embarking on a new Path, the Agent MUST execute the **Dual-Discovery Initialization** pattern before advancing to any codebase-mutating Activities.
   - **Backlog Generation Invariant:** When the Agent generates new items for the backlog (e.g., scoping activities), it MUST utilize the `--path` argument in `bin/backlog new` to bind it to a parent Path, preventing Orphaned Nodes.
   - **DAG Integrity Invariant:** To preserve DAG integrity, any script or process creating structural Path objects MUST apply the `path` and `backlog` labels identically to `bin/backlog new`, because the metasystem engine relies on strict label queries to resolve the topological DAG.
   - **Orthogonal Scope Verification Invariant:** Before provisioning new nodes via `bin/backlog new`, the Agent MUST run `bin/backlog list` or `bin/backlog view` on the parent Path to explicitly verify that identical or highly overlapping nodes do not already exist, preventing Orthogonal Scope Violations.

1. **Plan (Contract Formulation):** 
   - Execute the shell script: `SPAO_PERSONA_ID=frontier ./bin/node plan-start "ISSUE_ID"` from the repository root to lock the backlog issue. Follow up with `SPAO_PERSONA_ID=frontier ./bin/node plan-finish "ISSUE_ID" "Body content..."` to upload the finalized Node Contract. This automatically prepends the Node ID to the GitHub Issue title.
   - **Meta-Rule Invariant:** Node Issues MUST be pulled from the backlog. It is mathematically forbidden to generate a new issue out of thin air during the Plan phase. The Node ID is mathematically isomorphic to the GitHub Issue ID.
   - **Template Invariant:** The Agent must NEVER generate inline markdown strings for GitHub Issues. All issue bodies (Backlog and Node Contracts) MUST be rendered using strict, Operator-editable templates located in `kb/templates/`.
   - **Semantic and Command Purity Invariant:** Any specifications added under `kb/` (e.g. `WHAT-` files) during planning must not introduce deprecated terms defined in `kb/semantic_ledger.yml` or raw shell command strings (such as `git-fetch`), which trigger static KB conflict validation failures.
   - Mutate the body of the **Path Issue** to link to the newly active Node Issue via `./bin/meta link "Node X: Title" "ISSUE_ID"`.
   - Execute the checkout command to establish the worktree: `SPAO_PERSONA_ID=frontier ./bin/node checkout "ISSUE_ID" "branch_name"` from the repository root, ensuring "branch_name" conforms to the `node/<id>-<kebab-case>` format to pass validation. To ensure checkout resilience against pre-existing branch indexes, the git client automatically detects and cleans up stale local branches during worktree creation.
   - **Remote Branch Pruning Invariant:** Prior to checkout or push operations, the Agent MUST verify that any stale or divergent remote branches matching the target branch name on GitHub are explicitly pruned or deleted to prevent non-fast-forward rejections during reflection.
   - *Do not execute codebase mutations until the Node Issue is explicitly locked and the worktree is checked out. Under the Universal Merge Gate (HTIL) model, the Agent may autonomously transition from Plan to Act once the NC is locked, without waiting for chat approval.*

3. **Act (Execution):** 
   - Execute codebase generation, tool invocations, and artifact mutations required by the Scope.
   - **TDD Invariant:** You MUST use `./bin/run-tests` for all local testing. Raw bash `pytest` is strictly forbidden.
   - **Worktree Test Context:** To verify worktree logic mutations, execute tests from within the checked-out worktree directory itself rather than running them targeting the worktree files from the repository root directory.
   - **Asynchronous Prompt Interception:** If the Operator submits an asynchronous prompt or system signal during the Act phase, you must strictly preserve the `WIP-N=1` invariant. Queue the prompt into `artifacts/prompt_backlog.md` (via `./bin/prompt "..."` or local write) and immediately return to the active task without altering cognitive context.

4. **Observe (Automated Phase):** 
   - **Prompt Backlog Flush:** The Agent must read and flush `artifacts/prompt_backlog.md`. Collate and deduplicate the queued prompts. If they are executable system commands (e.g., `backlog new`), execute them. If ambiguous, address them conversationally in the chat. Finally, wipe the file contents clean.
   - The Agent automatically proceeds to the Reflect phase if all local tests (`./bin/run-tests`) pass and there are no unhandled prompt directives. The Observe phase is no longer a manual HITL pause, as structural validation is deferred to the Universal Merge Gate (HTIL) after reflection.

5. **Reflect & Advance (Post-Condition):** 
   - Execute the shell script: `SPAO_PERSONA_ID=frontier ./bin/node reflect "ISSUE_ID" "Node X: Title" "Learnings..." "['[x] Invariant']" "commit message" "node/XX-kebab-case" --insights WHY-XXXX` exclusively from the repository root directory. Execution from within active worktrees is strictly prohibited to prevent path double-nesting.
   - This atomic skill will rigorously enforce branch naming, update `artifacts/frontier_state.md`, push the branch, and automatically open a Pull Request.
   - Mutate the **Path Issue** body to check off the completed node.
   - **HARD HITL BLOCK (Universal Merge Gate):** The Agent must absolutely halt and wait for the Operator to review and merge the PR on GitHub before proceeding to the next node. The Pull Request merge is the sole hard integration gate.
   - **The Rollback Invariant:** If a command or API failure triggers a transaction rollback during the reflect phase, the Agent MUST execute the state recovery protocol: (1) delete the remote branch on GitHub, (2) reset the local worktree branch to `origin/main`, (3) document the failure in `artifacts/audit/retro-<id>.md`, and (4) only then re-execute the reflection command.


## Executing the Formal Bootstrap Audit
Before a newly bootstrapped repository can transition into active "Operations," it must pass an audit.
1. The Agent must fetch the `HOW-0002-bootstrap-audit-template.md` from the `dyad-wu-wei` meta-repository.
2. The Agent opens a new Node Issue using this template.
3. The Agent performs the compliance checks against the codebase and checks off the boxes in the issue body.
4. The Agent pauses (Observe phase) for a final Operator HITL sign-off before closing the audit ledger.
