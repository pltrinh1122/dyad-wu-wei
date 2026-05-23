# Probe 125: Architectural Evaluation of Hot-Fix Workflow

## Background
During a recent operation, the Frontier Agent bypassed the formal Sense-Plan-Act-Observe (SPAO) loop and executed a direct commit/push to the `main` branch to update the `GEMINI.md` hook. This "hot-fix" operation allowed a concurrent thread to immediately pick up the new instructions. 

This Probe evaluates whether this behavior should be formally adopted as a "Hot-Fix Workflow" or strictly outlawed.

---

## Pros of Allowing Hot-Fixes

1. **Velocity on Trivial Changes**: Operations like fixing typos, updating documentation (`GEMINI.md`, `README.md`), or adjusting `.gitignore` do not warrant the heavy overhead of creating an Issue, planning a Node, generating a PR, and executing `sync-clean`.
2. **Concurrent Thread Unblocking**: As demonstrated, a hot-fix allows the immediate propagation of systemic instructions to parallel execution threads without forcing a repository-wide PR sync cycle.
3. **Backlog Hygiene**: It prevents the `bin/backlog` from becoming bloated with low-value, zero-complexity tasks that distract from core structural paths.

## Cons of Allowing Hot-Fixes

1. **Violation of SPAO Meta-Loop**: Direct commits bypass the formal architecture, specifically the `reflect` phase which enforces invariants and captures learnings.
2. **Loss of Traceability**: Direct commits lack a corresponding GitHub Pull Request and Issue, making historical audits significantly harder.
3. **Ledger Drift**: The `artifacts/frontier_state.md` ledger does not track hot-fixes, meaning the system state might drift from the documented frontier.
4. **Race Conditions**: In a parallel execution environment, allowing uncontrolled direct commits to `main` significantly increases the risk of `git push` conflicts and race conditions if multiple agents attempt to mutate the tree simultaneously.

---

## Architectural Recommendation

**Verdict: Formalize a Tiered Governance Model.**

Instead of strictly outlawing hot-fixes or allowing them uncontrolled, we should formalize a **Tiered Governance Model**:

### Tier 1: The SPAO Node (Default)
All code changes, feature work, architectural probes, and orchestration updates **MUST** follow the strict SPAO loop using `bin/node` and formal PRs.

### Tier 2: The Formalized Hot-Fix
We should create a new primitive: `bin/hotfix`. 
- **Constraint**: It is strictly limited to non-executable files (`*.md`, `.gitignore`, `docs/`).
- **Mechanism**: The agent uses `./bin/hotfix <file> <commit_message>` to bypass the ledger and commit directly to `main`.
- **Traceability**: The `bin/hotfix` script will automatically append the commit hash to a new lightweight ledger (e.g., `artifacts/hotfix_ledger.yml`) to ensure traceability is maintained without the heavy PR overhead.

### Next Steps
If this recommendation is approved, we should queue an Activity Node to implement the `bin/hotfix` utility and its associated traceability ledger.
