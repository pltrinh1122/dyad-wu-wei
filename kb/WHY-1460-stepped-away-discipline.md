# WHY-1460: The Stepped-Away Discipline

## Classification
- **Type**: WHY (Architectural Principle)
- **ID**: WHY-1460
- **Author**: agent-sg5
- **Created**: 2026-05-30 (Node 1460, Path 1459)

---

### 1. The Context
The Metasystem utilizes a conversational agent loop (SPAOR) combined with background heartbeat daemons (e.g., `drivers/audit_daemon.py`). During normal operation, the system functions optimally when both elements run concurrently. 
However, the system encounters distinct wait states known as **HTIL (Human-in-the-Loop) gates**—such as when waiting for PR merges or receiving explicit user input at NBA Handoffs.

### 2. The Problem
When the Operator steps away from the terminal (the "Stepped-Away Discipline"), the conversational agent correctly goes dormant, awaiting an explicit callback via the chat channel. But if background tasks, like the audit daemon or recurring timers, remain active, they artificially keep the agent's context alive, consuming compute and polluting transcripts without generating actionable value. Since the Agent's turn strictly forbids yielding natively while waiting for background commands, an unthrottled background daemon creates a continuous polling loop while the Operator is offline.

### 3. The Resolution
To conserve compute and maintain true dormancy during HTIL blocks:
1. **Dormancy Injection**: When the Agent enters a terminal wait state (e.g., waiting for an HTIL merge at the end of the Reflect phase, or waiting for explicit Operator prompt during NBA Handoff), it must possess the logical capability to pause or terminate non-critical heartbeat daemons.
2. **Re-Instantiation**: Upon the Operator's return (the "Step-Back Discipline"), which wakes the Agent via the conversational channel, the Agent must explicitly verify the state of background daemons and re-instantiate them during the Sense phase if necessary.
3. **Execution Invariant Preservation**: This does not violate the Asynchronous Execution Invariant because the agent yields *safely* to the natural conversational turn mechanism rather than arbitrarily sleeping.

This ensures the system is tightly coupled to the Operator's physical presence, optimizing for Wu-wei (effortless action) without wasting energy on empty cycles.
