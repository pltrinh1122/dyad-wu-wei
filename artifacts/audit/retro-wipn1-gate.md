# Retrospective: WIP-N=1 HTIL Gate Policy Violation

## Violation
The Frontier Agent halted execution and surfaced a HARD HITL block for PR #2318 (`node/2313-reflect`), requesting the Operator to review and merge the PR before `checkout` of Node 2274 could proceed. 

## The Operator's Correction
The Operator issued a correction stating that the only remaining HTIL Gate conditions for PRs are for changes to `GEMINI.md`, `CLAUDE.md`, or `DYAD.md`. PR #2318 only modified `artifacts/reflect_2313.md` and `artifacts/telemetry_frontier.jsonl`, and thus should not have triggered an HTIL block.

## Codified Insight
1. **Gate Reduction**: The `WIP-N=1` invariant and Universal Merge Gate must logically differentiate between PRs that modify core engine instructions (`GEMINI.md`, `CLAUDE.md`, `DYAD.md`) versus PRs that only modify artifacts or regular code.
2. **Action Item**: The hardcoded `WipN1Guard` in `kernel/node_lifecycle.py` is currently a blanket ban on *any* open PRs. This guard must be updated to inspect the modified files of the open PRs. If the open PRs do not touch the restricted files, the engine should auto-merge them or the guard should bypass the block. 
3. **Immediate Remediation**: The Frontier Agent will autonomously merge PR #2318 to unblock the execution floor.
