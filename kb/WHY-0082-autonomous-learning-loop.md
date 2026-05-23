# WHY-0082: Autonomous Learning Loop

## 1. Problem Statement
The standard execution loop relies on explicit error signals (e.g., CI failures, Python syntax errors) to trigger self-correction. When these errors occur, the telemetry native hook forces an Audit Retro file. However, soft-policy violations (e.g., executing a command outside of the designated sandbox, missing a KDR, failing to follow a documented procedure) typically exit with code `0`. When the Operator corrects the Agent via chat for a soft-policy violation, the Agent learns in the ephemeral context of the chat session, but fails to mutate the system's permanent memory. This directly violates **SG-0005 (Knowledge Mutation)**.

## 2. The Decision
To permanently eliminate the risk of recurring soft-policy failures, we mandate the **Autonomous Learning Loop**. This is a formal mechanism to enforce that *all* chat-based corrections trigger permanent architectural state mutation. 

If the Operator provides a chat correction regarding a policy violation or workflow failure, the Agent must immediately transition into an **Epistemic Reflection** state. The Agent is required to codify the violation and the correction into an `artifacts/audit/retro-<id>.md` file, which serves as immutable evidence of learning, *before* sending its chat response.

## 3. Architectural Implications
1. **The Agentic Retro Trigger**: A permanent contextual ROM instruction must be injected into `GEMINI.md` to mathematically bind the Agent to this behavior.
2. **Epistemic Reflection Node**: The SPAO `Observe` gate must be upgraded. We must implement `bin/node retro` as a native command, allowing the Agent to formally attach the Retro file to the current branch and execution ledger.
3. **Ledger Synchronization**: All retro files created via this loop must be structurally linked to the active Node ID to maintain the single-thread continuity of the Path execution ledger.
