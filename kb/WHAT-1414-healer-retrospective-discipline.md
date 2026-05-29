# WHAT-1414: Healer Dyad Retrospective Discipline

## 1. Intent
To formally codify the **Healer Dyad Retrospective Discipline**, providing a structured mechanism for the Healer/Operator to hand off context back to the Frontier Agent after resolving a state-of-exception (seizure or loop collapse).

## 2. Distinction from SHAR
While the SHAR Compiler (WHAT-0047) evaluates the normative SPAO loop via automated telemetry, the Healer Dyad Retrospective is an out-of-band qualitative handoff. It is authored by the Operator (acting as Healer) upon stepping down, bridging the semantic gap between the exception state and the resumed normative loop.

## 3. Structural Primitives
The retrospective is strictly formatted into four conceptual blocks (template: `kb/templates/healer_retrospective.md`):
1. **Marker**: A classification of the event (e.g., seizure-restart vs. routine reboot) and the precise root cause.
2. **What Worked (Reinforce It)**: Identification of systemic guards, detection mechanisms, or autonomous stabilization behaviors that functioned as designed and should be reinforced.
3. **What Was Resolved Well (Tactical Validation)**: Confirmation of tactical interventions that successfully bounded the recovery without violating patient agency.
4. **New Truths / State Changes (Weigh in Loop)**: Any ongoing constraints, deferred tasks, or known technical debt (e.g., deactivated crons, bypassed guards) that the Frontier Agent must ingest into its ongoing context without needing explicit, imperative instructions.

## 4. Execution
The retrospective is instantiated by the Operator in the chat interface and transposed by the Frontier Agent into `artifacts/audit/retro-<case-id>.md` upon resuming the SENSE phase.
