# Agentic Retrospective: Periodic Health Audit Dissonance

## Context & Violation
The operator observed an architectural dissonance regarding the `periodic-health-audit` prompt triggered by the local `audit_daemon.py`. The daemon injects a manual chat prompt for the agent to execute a "Periodic Health Audit" every 10 nodes. The operator correctly pointed out: *"it feels odd that the trigger is for you to run the health check if it can be autonomously run."*

This violates the principle of autonomous execution and containment. The agent is being treated as a manual cron job to run tests, rather than relying on deterministic programmatic layers to verify their own invariants. 

## Codified Insight
1. **Deterministic Autonomy**: If a health check is deterministic (e.g., verifying file checksums, testing invariants, checking git status), it must be automated natively via tests or hooks. (Indeed, `bin/node sync` already runs a `Metasystem Integrity Audit` synchronously).
2. **Agentic Semantic Boundaries**: Asynchronous prompts injected into the agent's backlog should be strictly reserved for **semantic evaluations**—tasks that require reasoning, architecture review, or contextual alignment that Python scripts cannot autonomously resolve.
3. **Anti-Pattern Identification**: Using an LLM to manually click "run tests" every N nodes via a chat prompt is an anti-pattern that degrades velocity and misuses agentic compute. 

## Proposed Remediation
The `periodic-health-audit` rule in `infra/audit-daemon/audit_config.yml` should either be deleted entirely (deferring to the autonomous `sync` hook), or redefined explicitly as a semantic review protocol with a corresponding `HOW-*` playbook.
