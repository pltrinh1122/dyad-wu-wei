# Discovery 1023: Harmonize - Refine DZ-CIL Intent Understanding

## 1. Current State of Chat Immediacy Protocol
According to `WHAT-1037-chat-immediacy-protocol.md`, the Agent must respond to Operator commands instantly with the following format:
`Hai. (Intent: <Interpretation>. Status: <Action taken>.)`

The specification mandates that the `<Interpretation>` field must factor in "the active DZ-CIL context, Ziran, and the Dao." However, the exact mechanics of this factoring are left undefined.

## 2. Identified Gaps (The Antithesis)
Currently, there is no formal codification of how the Agent translates raw Operator input into a "DZ-CIL Intent" that explicitly demonstrates understanding of both the Dao and Ziran.
- **The Dao Gap**: The interpretation often fails to ground the action in the rigid SPAO state machine, the active Path, or the specific Node. It lacks the structural context (The Dao).
- **The Ziran Gap**: The interpretation fails to acknowledge the current active frontier state or the natural flow of the execution (Ziran). It treats Operator commands as isolated zero-context events rather than continuations of the continuous inference loop.
- **The Syntactic Gap**: Because the definition of "DZ-CIL context" is vague in `WHAT-1037`, Agents may revert to generic summaries (e.g., "Fix telemetry") instead of Agentic state summaries (e.g., "Executing Act phase for Node 1023 to fix telemetry").

## 3. Required Modifications (The Synthesis for Plan Phase)
To successfully refine DZ-CIL Intent Understanding, we must update `WHAT-1037-chat-immediacy-protocol.md` to explicitly require the following dimensions when formatting the `<Interpretation>`:

1. **The Dao Assertion**: The intent must explicitly state the structural boundary it is operating within (e.g., referencing the specific Node, Path, or SPAO Phase).
2. **The Ziran Context**: The intent must demonstrate awareness of the current state of the repository and the logical next-step momentum of the flow.
3. **Format Hardening**: We must provide concrete examples in `WHAT-1037` demonstrating how to weave Dao (structure) and Ziran (flow) into a single concise intent string.

This concludes the Harmonize phase. We are prepared to proceed to the Plan phase (Node 1024) to lock in the architectural contract for these specification updates.
