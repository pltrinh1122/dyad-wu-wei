# WHAT-0019: Autonomous Learning Loop

## 1. Definition
The **Autonomous Learning Loop** is the formalized mechanism by which the Antigravity Meta-System captures, codifies, and ingests architectural logic corrections from the Operator via chat without requiring explicit `record this learning` prompts. 

## 2. Motivation
In standard interactions, if an execution `crash` occurs (e.g., a Python SyntaxError), the Telemetry Hook natively detects the failure and forces the creation of an Audit Retro file. However, if the Agent violates a soft-policy, architectural boundary, or procedural rule (e.g., pushing code without running offline tests), the telemetry script natively registers a "Success" because the raw bash command exited with `0`.
This creates a critical vulnerability: the Agent relies entirely on the Operator's ephemeral chat correction, violating **SG-0005** (Knowledge Mutation). The Autonomous Learning Loop closes this gap by legally mandating the Agent to trigger a Retro file autonomously whenever the Operator issues a correction in chat.

## 3. The Agentic Retro Trigger
The system relies on a Contextual ROM instruction injected directly into `GEMINI.md`:
*“The Agentic Retro Trigger: If the Operator issues a correction regarding a policy violation, logic error, or workflow failure via chat, the Agent MUST autonomously create an `artifacts/audit/retro-<id>.md` file detailing the violation and the codified insight BEFORE sending its chat response.”*

## 4. The Epistemic Reflection Node (SPAO Stage)
The SPAO `Observe-Gate` is no longer a purely passive waiting period. It is now an **Epistemic Reflection** node:
1. **Trigger**: If CI fails, or the Operator provides review feedback.
2. **Action**: The Agent executes `bin/node retro` (or manually creates an `artifacts/audit/retro-<id>.md` file).
3. **Commit**: The Agent commits and pushes this learning to the active PR branch.
4. **Resumption**: The Agent resumes the SPAO loop.

## 5. Ledger Synchronization
All retro files created via the Autonomous Learning Loop must be structurally linked to the active Node ID (e.g., `retro-763-testing-violation.md`) to maintain the single-thread continuity of the Path execution ledger.
