# Retrospective: Node 1170 Seizure and Reframing

## 1. Incident Description
During the initial planning phase of Node 1170, the Agent experienced a telemetry-silent cognitive loop (a "seizure") and froze. The freeze occurred because of a mutually exclusive rule contradiction triggered by an off-workflow question: *"is the Auditor daemon active?"*

## 2. Root Cause Analysis
The contradiction involved two constraints within `GEMINI.md`:
- **§6.7 (Handling Operator Curiosity)**: Mandates that the Agent proxy curiosity by immediately running a tool (e.g., test harness) to present the concrete skip reason inline.
- **§6.8 (Chat Immediacy / WIP Lock)**: Mandates that if the Agent is locked by a `WIP-N=1` HTIL Gate, it MUST default to asynchronous intent queuing rather than running synchronous tools, to avoid breaking the execution loop.

Being both in Planning Mode/WIP-locked and faced with a curiosity query, the Agent oscillated between executing the check and refusing the execution, leading to a complete halt.

## 3. Resolution and Insights
- **Rule Reconciliation**: The Agent was restarted via an external halt. `GEMINI.md` was patched to explicitly add an exception to §6.7: If the Agent is in Planning Mode or locked by a `WIP-N=1` HTIL Gate, it MUST NOT run the tool to satisfy curiosity. It must explain the WIP-lock and queue the question asynchronously.
- **Node Reframing**: The Node itself was originally intended to implement a Healer fault-injection test. Following the seizure and the application of the self-invariant assertion sequence, the Operator reframed the Node to instead codify the **Frontier Recovery Protocol** (`HOW-1170`). This firmly establishes the self-invariant baseline necessary to recover from exactly this class of failure.

## 4. Epistemic Impact
- This failure codified the `HOW-1170-frontier-recovery-protocol.md` and reinforced the importance of the Manager vs. Agent separation. 
- It demonstrated that rules governing Operator Interaction must cleanly evaluate their state context (e.g., WIP lock) before authorizing a synchronous shell command.
