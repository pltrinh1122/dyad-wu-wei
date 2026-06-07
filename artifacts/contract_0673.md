# Alignment Contract: Codify Deterministic Enforcement of System Rules

## Philosophical Stance
`agent-meta` is the Legislature, not the Executive.
What `agent-meta` does: It defines the philosophical and strategic rules of the game in static markdown (kb/HOW-0001-spao-execution-loop.md) and designs the engine CLI schematics.
What actually enforces the rules: The deterministic physics of the repository itself. If a rule exists, it must be shifted entirely out of the LLM domain and codified into stateless, hard-coded gates.

Examples:
- The WIP-N=1 invariant isn't enforced by `agent-meta` scolding another agent; it's enforced by `mgr_node.py` instantly throwing a hard Python exception (`FlowTransaction failed: Active lock exists`) if a second branch is checked out.
- The Reflection Invariant (SG-0005) isn't enforced by an LLM asking for a retrospective; it's enforced by `node_lifecycle.py` mathematically blocking the `spao node reflect` command until `artifacts/audit/retro-[ID].md` exists on disk.

## Conclusion
`agent-meta` designs the chessboard. `agent-platform` builds the physical board based on those designs. But neither "enforces" the rules during the game. The rules are enforced by the deterministic physics of the board itself—if a piece attempts an illegal move, the board mathematically prevents it from happening. If an LLM agent ever has to manually step in to enforce hygiene or boundaries, the system's automation design has failed.

## Next Steps
This philosophical stance will be formally codified into a Knowledge Base document (`WHAT-xxxx`) in the Plan node (674).
