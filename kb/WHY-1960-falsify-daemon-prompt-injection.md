# WHY-1960: Falsification of Daemon Prompt Injection

## The Premise
Our background metasystem integrity daemon (`drivers/audit_daemon.py`) is responsible for monitoring system health, evaluating lexical guards, and detecting Sluice Gate (PR merged) events. Historically, when the daemon detected an event, it notified the system by injecting a payload (e.g., `[NOTIFICATION] Sluice Gate Opened`) directly into the Operator's asynchronous prompt queue (`artifacts/prompt_backlog.yml`). 

## The Friction (Authorization Gate Collision)
Dyad-Cairn hypothesized and proved that feeding machine-structured NBAs or daemon alerts into the human Operator's `prompt:` queue creates an **Authorization Gate Collision**. 
- The `prompt:` queue requires a **Design-Review Gate** (conversational parsing, ambiguity resolution).
- Daemon alerts require an **Execution Gate** (deterministic DAG mutation).
By conflating these two streams, the Agent encounters execution seizures, attempting to converse about physical state changes rather than executing them.

## Dialectical Falsification
1. **Falsification of WHY-0090 (Option D)**: `WHY-0090` originally selected "Reactive Event-Driven Synchronization" by having the Sluice Gate sensor write to the prompt queue, which `bin/node sync` would later read. This is formally falsified because it uses a conversational intent queue as a machine event bus.
2. **The Survivor (Orthogonal Substrate Integrity)**: The daemon must exclusively communicate by mutating the DAG (Frontier/Node/Backlog). It must never trespass into the `prompt:` queue.

## Chosen Harmonization Path
To reconcile this and achieve pure orthogonality:
1. The **Operator** exclusively mutates the `prompt:` queue (Intent Domain).
2. The **Daemon** exclusively mutates the DAG (Structural Domain) or directly executes silent substrate operations (e.g., `bin/node sync`).
3. The **Agent** strictly executes the active `WIP-N=1` Node (Execution Domain), insulated from both noise and asynchronous hygiene tasks.
