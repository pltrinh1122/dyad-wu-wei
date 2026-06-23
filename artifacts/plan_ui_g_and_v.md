# Architectural Design: UI Model for Generation & Validation (G and V)

## 1. Problem Statement
Current user interfaces (UI) that are driven purely by Generation (G) - such as standard chat interfaces taking natural language instructions and generating output - lack structured reliability. They can silently drift from operator intent because there is no immediate, tightly coupled Validation (V) phase acting as a forcing function to keep the generative output grounded. Without V, G flows inconsistently.

## 2. Core Concept
The new UI pattern binds Generation (G) and Validation (V) into a single, cohesive operator interaction loop. For every operator intent (G) submitted, the interface immediately surfaces the corresponding structural validation constraints (V), often embodied as "CSI Guards" (Cognitive State Invariants / Contract Structural Invariants) or test criteria. 

This model essentially states: **Every generated intent must be paired with an executable or structural validation constraint at the UI level.**

## 3. UI Interface Pattern & Implementation

### 3.1 Operator Interaction with the Backlog
When an operator adds an intent or node to the backlog, the UI enforces a split-pane or dual-entry system:
- **Left/Top (The Intent/G):** Natural language description of what is to be done.
- **Right/Bottom (The Constraint/V):** A required field defining *how* the system will validate that the intent has been successfully met (e.g., specific test file, CSI guard script, invariant condition).
- **State Requirement:** A node in the backlog cannot move to the "Executing" state without the V-component being explicitly linked.

### 3.2 CSI Guards Integration
CSI Guards act as the runtime verification of the V layer.
- **Visual Feedback:** In the terminal UI or dashboard, as the agent executes the generation step, the CSI guards are displayed in real-time as a checklist or progressive gauge.
- **Blockers:** If a CSI guard fails, the UI visually halts the Generation flow, explicitly surfacing the validation failure and enforcing self-correction before allowing further progression.

### 3.3 Terminal UI Flow
A potential CLI or Terminal UI pattern for this is the **"Prompt & Prove"** prompt:
1. `Operator > [G] Build the new API endpoint.`
2. `System   > [V] How will this be proven? Provide the CSI Guard or Test command.`
3. `Operator > [V] npm run test:api`
4. The system links these elements, ensuring that any artifacts generated from [G] are immediately tested against [V] in a tight execution loop.

## 4. Conclusion
By linking structural validation constraints directly to operator intents within the UI, we transition from pure open-ended Generation to bounded, verifiable Generation. This stabilizes the autonomous flow, minimizes deviations, and builds operator trust.
