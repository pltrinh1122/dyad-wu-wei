# WHY-0086: Epistemic Retrospective Synthesis

## The Premise
When an Agent encounters execution failures, the system's `enforce_reflection_hook` mandates the creation of a retrospective document (`artifacts/audit/retro-<id>.md`). This ensures that the context and root cause of the failure are preserved.

## The Problem
Currently, these retrospectives act purely as passive logs. They are written to the `artifacts/audit/` directory and left dormant. This represents an epistemic break in the state machine's Autonomous Learning Loop: if the failure context is never actively synthesized into system boundaries (`WHY` primitives or lexical guards in `audit_config.yml`), the system relies on human Operators or Agent working memory to remember the lesson, violating Ziran (natural flow) and Dao (structural coherence).

## The Invariant (Synthesis Surfacing)
To close the Autonomous Learning Loop, retrospectives must be actively processed. However, because Orchestrator system scripts must operate with zero-latency deterministic state, they cannot execute LLM inference directly to synthesize the learning.

Therefore, the system MUST autonomously push a synthesis `Activity` to the global Backlog whenever an un-surfaced retrospective is detected. By routing the retrospective into the Backlog, the Meta-Orchestrator safely delegates the non-deterministic synthesis work to the Agent's standard SPAO lifecycle. The Agent will pull the Activity, read the log, and mutate the structural invariants (the Dao) to ensure the failure pattern is structurally impossible to repeat.
