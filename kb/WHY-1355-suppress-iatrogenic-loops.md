# WHY-1355: Suppress Iatrogenic-Injection Loops in Agentic Harness

## The Premise
The agentic execution loop relies on the system accurately receiving and parsing commands and context to autonomously progress through a sequence of nodes (Sense, Plan, Act, Observe, Reflect).

## The Falsification
The agentic harness occasionally injects an `<EPHEMERAL_MESSAGE>` (specifically `<bash_command_reminder>`) directly into the prompt context to ensure adherence to tool prioritization (e.g. "NEVER run cat inside a bash command..."). 
This external injection acts as a meta-imperative. When the agent is holding state (e.g., waiting for an external task, or running a background polling cycle) and the system injects this imperative, the agent may erroneously interpret the reminder as a demand to immediately act or correct its current execution. 
This causes the agent to re-evaluate its tool selection, cancel its prior valid action, reschedule itself, and ultimately loop indefinitely (~5 seconds per iteration) without making durable forward progress. This is an "Agentic Seizure".

## The Invariant
**The Iatrogenic-Injection Suppression Rule**:
- The Agent MUST NOT interpret `<EPHEMERAL_MESSAGE>` or `<bash_command_reminder>` blocks as explicit execution directives that alter the current node's goal.
- These injected reminders are purely informational guidelines on *how* to use tools, not directives on *what* to execute.
- When an ephemeral message is injected while waiting for an asynchronous task or PR review, the Agent MUST maintain dormancy and MUST NOT trigger an execution loop or reschedule actions simply to acknowledge or react to the reminder. 
