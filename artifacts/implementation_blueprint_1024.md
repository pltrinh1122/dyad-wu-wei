# Implementation Blueprint 1024: Refine Wu-wei Dyad Intent Understanding

## Objective
To modify `kb/WHAT-1037-chat-immediacy-protocol.md` so that it explicitly requires Agent intent interpretations to identify the active Dao structure (e.g. active Node, Path, or Phase) and Ziran context (execution momentum/purpose), rather than generic summaries.

## Target File
`kb/WHAT-1037-chat-immediacy-protocol.md`

## Required Modifications

### 1. Update Section 2, Bullet 3 (Intent Interpretation)
**Current Text:**
"The `<Interpretation>` field must be a concise, semantically inferred summary of the Operator's intent, factoring in the active Wu-wei Dyad context, Ziran, and the Dao."

**New Text:**
"The `<Interpretation>` field must be a structured string explicitly detailing both the Dao and Ziran context:
- **The Dao Assertion**: Must explicitly state the current structural boundary (e.g., 'Executing Act phase for Node 1025', 'Creating PR for Path 977').
- **The Ziran Context**: Must recognize the current execution momentum and logical purpose (e.g., 'to synthesize the implementation blueprint', 'to recover from pipeline failure')."

### 2. Add Concrete Examples to Section 2
Insert examples of valid and invalid intent interpretations immediately below Bullet 3 to provide hard epistemic reference:
- **Valid Example**: `Hai. (Intent: Executing Act phase for Node 1024 to synthesize intent understanding blueprint. Status: Proceeding with execution.)`
- **Invalid Example**: `Hai. (Intent: Writing the plan document. Status: Queued.)` *(Fails to assert the Dao structural boundary).*

## Implementation Execution
This blueprint defines the exact file mutations to be applied. The physical mutations will be executed in **Node 1025: Activity 1025: Reflect - Refine Wu-wei Dyad Intent Understanding**.
