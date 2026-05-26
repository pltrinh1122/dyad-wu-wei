# WHY-1145: Falsification of Prompt Queue Processing Outcomes

## 1. The Thesis
**Thesis:** Prompt queue processing should be quick and should result in an inline chat response with a link to details if it's a report. Otherwise, the outcome should be a Backlog item.

## 2. The Antithesis
If all non-report prompts are blindly converted into Backlog items, the Operator is forced into an overly bureaucratic process for trivial tasks (e.g., correcting a single typo in a document), destroying inner-loop velocity (SG-0003). Conversely, if the Agent attempts to process complex functional changes "quickly" to satisfy an inline chat response, it bypasses the SPAO execution loop, violating the PR Merge Gate, the Containerized Testing Invariant (SG-0002), and the WIP-N=1 rule, resulting in unverified, untracked mutations.

## 3. The Synthesis
Prompt queue processing must respect the Materialization Boundary and the Hot-Fix Workflow Evaluation (WHY-0010/Probe 125). The outcome of a prompt is not binary, but dynamically routed based on complexity:
1. **Investigatory / Report:** Quick execution. The agent generates the data, writes it to `artifacts/`, and provides a passive link in chat.
2. **Trivial Documentation Mutation:** The agent executes the change immediately using the `bin/rt` (Runtime Hotfix) primitive, directly pushing to `main` and recording it in the hotfix ledger, preserving traceability while maintaining high velocity.
3. **Complex / Functional Mutation:** The prompt MUST NOT be executed inline. It must be formally codified into a GitHub Issue (`bin/backlog new`), adding it to the global dependency graph. The prompt is then consumed, and the actual execution is deferred until that Node is prioritized and checked out via the standard SPAO loop.
