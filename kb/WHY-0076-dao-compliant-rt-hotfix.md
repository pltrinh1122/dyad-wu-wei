# WHY-0076: Dao-Compliant Runtime Hotfix

## The Violation
The `spao rt hotfix` mechanism was designed as a Tier-2 direct-to-main path for low-risk corrections. Under the ratified HOW-0006 decision-making invariant, this mechanism fails all three gates:

1. **NS-0001 (Telic Ground)**: Direct-to-main commits remove the Operator from the decision loop entirely. The Synergistic Human-Agent Partnership requires HITL at every mainline mutation — even for documentation.
2. **Wu-wei (Energy Constraint)**: Friction appears eliminated for the Agent, but it is exported invisibly to the Operator — code lands on main without the Operator seeing a diff, reviewing intent, or approving correctness.
3. **Ziran (Coherence)**: No Operator declaration authorizes bypassing HITL review on the mainline. GEMINI.md explicitly requires HITL blocks.

This was surfaced in practice during Node 844, where `spao rt hotfix` was attempted for the HOW-0006 Epistemic Scope amendment, failed due to the main branch being locked by a worktree, and required a fallback PR path. The PR path proved superior in every dimension.

## The Secondary Violation
`execute_insight` in `daemon_rt.py` also required the caller to be on the `main` branch and returned to `main` via `git_client.switch("main")` after creating the PR branch. This fails when main is locked by an active worktree — the same environmental condition that routinely exists during SPAO loop execution.

## The Architectural Decision
Both `execute_hotfix` and `execute_insight` must be **branch-first, PR-gated**:

1. The caller does NOT need to be on `main`
2. A timestamped branch is created off `origin/main`
3. The change is committed to that branch
4. The branch is pushed and a PR is created for Operator review
5. The Operator merges — HITL is preserved
6. No `switch` back to main is needed

This makes `spao rt` a **PR-creation tool**, not a **direct-push tool**. The distinction is the Dao.

## Scope
- `kernel/daemon_rt.py`: `execute_hotfix` rearchitected to PR-based flow; `execute_insight` main-branch guard removed
- `kb/WHY-0076-dao-compliant-rt-hotfix.md`: This document

## Invariant Exemption (WIP-N=1)
Because `bin/rt hotfix` explicitly bypasses the SPAO Node-Loop to operate directly as a Tier-2 mechanism, it does not acquire the `WIP-N=1` lock. Tier-2 Hotfixes may therefore be authored and merged concurrently (e.g., merging multiple hotfix PRs at once) without violating the `WIP-N=1` discipline.
