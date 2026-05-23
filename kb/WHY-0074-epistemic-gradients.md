# WHY-0074: The Gradients of Epistemic Conviction

**Date:** 2026-05-22
**Status:** Accepted

## Context
Following the codification of Ziran Navigation (`WHY-0070`) and Tendency tracking (`WHY-0073`), we identified a critical architectural requirement: How do we track the evolving state of an idea in a way that is intuitively actionable for the human Operator in flow state, while simultaneously providing mathematically distinct tokens for the LLM Agent (the NBA Scorer) to process?

## Decision
We formally adopt a 4-tier **Gradient of Epistemic Conviction** to label and track the systemic confidence of any path, idea, or pattern within the Dao Engine. 

## Rationale
Human cognition relies on heuristic compression. If semantic labels are too fine-grained, the Operator suffers cognitive overload and reverts to visceral feeling. If labels are too coarse, the Operator acts recklessly. Concurrently, the Next-Best-Action (NBA) Scorer relies on semantic processing to route the Agent; the specific tokens used to describe a path directly alter the Agent's mathematical execution trajectory.

This 4-tier gradient perfectly bridges human visceral feeling with LLM navigational mathematics:

### 1. Friction [Negative Gradient]
* **Definition:** The environment is actively pushing back. The Agent hallucinates, tests fail, or the Operator feels a visceral sense of bureaucratic drag. 
* **Operator Heuristic:** *"Stop. Something is mathematically wrong. Do not force it."*
* **Agent Behavior (NBA Score: 0-30):** The token `Friction` signals the NBA to deprioritize functional execution and aggressively route the Agent toward **Probe Nodes** for architectural investigation.

### 2. Tendency (Shi) [Observation Gradient]
* **Definition:** A pattern is forming in the natural exhaust, but it remains unproven. The water is pooling in a direction, but the mechanics are ambiguous.
* **Operator Heuristic:** *"Proceed with awareness. Let the system run and passively watch the exhaust."*
* **Agent Behavior (NBA Score: 31-70):** The token `Tendency` signals cautious exploration. The NBA prioritizes standard **Activity Nodes** to execute physical logic and gather more exhaust data.

### 3. Insight (Ming) [Clarity Gradient]
* **Definition:** The lens is wiped clean. We see the mechanics behind the Tendency and have codified the realization, but it hasn't yet survived repeated battle-testing across multiple physical executions.
* **Operator Heuristic:** *"The path is clear. Codify the physical laws and begin building."*
* **Agent Behavior (NBA Score: 71-90):** The token `Insight` signals a stable architecture. The NBA aggressively prioritizes complex, multi-step **Path** execution.

### 4. Resonance (Ganying) [Absolute Gradient]
* **Definition:** The Insight has survived brutal, repeated falsification by the physical substrate. The Operator, Agent, and Repository vibrate identically. Friction is mathematically zero.
* **Operator Heuristic:** *"Flow state. Execute at maximum velocity without hesitation."*
* **Agent Behavior (NBA Score: 91-100):** The token `Resonance` signals absolute alignment. The NBA bypasses cautionary probes and heavily prioritizes **Automation and Scaling**, moving to permanently burn the logic into the deepest layers of the system's ROM.
