# Discovery: Decouple Prompt Channel to GitHub API and Instantiate Singular Staging Area

## 1. Intent Formulation
The system currently utilizes two fragmented and physical intake queues:
1. `status: todo` GitHub Issues for bugs and feature requests.
2. `artifacts/prompt_backlog.yml` for synchronous conversational prompts and HTIL steering.

The physical prompt backlog creates Git push collisions during concurrent swarm fan-out. Furthermore, overloading `status: todo` for both "raw unrubbed thought" and "formal pending execution node" (the DAG factory floor) creates severe cognitive dissonance in the taxonomy. 

## 2. Structural Analysis
We must synthesize a **Singular Staging Area** materialized entirely within the GitHub API:
- **The `staging` Label:** All raw intake (bugs, fleeting thoughts, and HTIL prompts) will enter the system as GitHub Issues tagged with `staging`. This creates a crisp, undeniable boundary between the Pre-Agentic Staging Area and the Execution Factory Floor (`status: backlog` or `status: todo`).
- **The Execution Gate:** The Engine's `plan-start` mechanism will query `gh issue list --label "staging"`. If the Staging Area is non-empty, the Engine will throw a `StagingAreaBlockedError`, halting the DAG factory floor. This guarantees that all Operator steering is consumed before new execution locks are acquired.

## 3. Implementation Blueprint
- **Deprecate Physical Backlog:** Delete `artifacts/prompt_backlog.yml`.
- **Refactor `bin/prompt`:** Rewrite the CLI to interact with the GitHub API. `bin/prompt queue <msg>` will execute `gh issue create --title "Prompt: <msg>" --label "staging"`. `bin/prompt process` will query and display the oldest `staging` issue.
- **Update Execution Gates:** Refactor `get_prompt_backlog_size` in `kernel/daemon_status.py` to count issues with the `staging` label. Update the error message in `kernel/node_lifecycle.py` to refer to the "Singular Staging Area" instead of the "prompt queue".

## 4. Next Actions
- [x] Create Plan node.
- [ ] Translate blueprint into explicit architectural mutations.
