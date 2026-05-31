## Goal
Prevent schedule/kill/re-schedule cycling seizures caused by harness re-injection of EPHEMERAL_MESSAGE meta-imperatives. The patient obeys the meta-imperative, re-evaluates tool selection, cancels prior action, reschedules, and loops (~5s per iteration, zero durable change). Root cause: harness bash_command_reminder injects a meta-imperative that contradicts the Dao's execution flow. Source: Intake #1307 (Healer, case-03).

## Meta-Index


## Agent Retrospective

### Continue
- Emphasize the inviolability of execution flow when interacting with unpredictable system harnesses.
- Use explicit Iatrogenic-Injection Suppression Rules in GEMINI.md rather than trying to engineer around the prompt injection.

### Stop
- Allowing injected ephemeral prompts to cancel in-flight wait states or asynchronous tasks, leading to execution seizures.

### Start
- Formalizing system-injected messages as pure information rather than directives.

- [x] Node 1356: Discovery 1356: Harmonize - Suppress Iatrogenic-Injection Loops in Agy Harness
- [x] Node 1357: Discovery 1357: Plan - Suppress Iatrogenic-Injection Loops in Agy Harness [Depends: 1356]
- [x] Node 1358: Activity 1358: Reflect - Suppress Iatrogenic-Injection Loops in Agy Harness [Depends: 1357]
