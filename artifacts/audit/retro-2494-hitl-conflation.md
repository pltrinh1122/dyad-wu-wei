# Retro: HARD HITL vs. Auto-Merge Conflation

**Trigger**: Operator issued a `[BUG]` correction via chat: *"if PR #2494 is a HARD HITL BLOCK, then it shouldn't have been auto-merged. if PR #2494 is NOT a HARD HITL BLOCK, then agent shouldn't have presented the block to Operator."*

## The Violation (Logic Error)
The Primary Agent presented a `HARD HITL BLOCK` message to the Operator, demanding a manual review and merge for PR #2494. However, PR #2494's actual state in GitHub was already `MERGED` (auto-merged). 

The Agent committed a state-desync fallacy: it outputted a static procedural template (the HITL block) without physically asserting the real-world state of the Pull Request.

## The Codified Insight
1. **State-Assertion Precedence**: The Agent's internal state machine must never assume a PR is open. Before presenting a `HARD HITL BLOCK` message, the system MUST verify the PR state via `gh pr view <id> --json state`. 
2. **Seamless Transition**: If the PR state is already `MERGED` (e.g., due to automated repository rules, an `rt` administrative bypass, or prior autonomous merge), the Agent must completely bypass the HITL block and automatically drop into the Reflect phase.
3. **Mutual Exclusivity**: A PR cannot be both auto-merging and a HARD HITL block. If the architecture designates a specific class of Nodes (like `refactor/rt-*`) for auto-merge upon CI success, the Agent must programmatically recognize this Node type and suppress the HITL prompt entirely.

## Next Action
Per `DYAD.md` Rule 24 (Administrative Node NBA), this `[BUG]` path must be dispatched to a dedicated sub-agent to formulate the Harmonize and Plan phases, bypassing the Strategist's cognitive bottleneck.
