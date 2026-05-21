# WHY-0047: Automated Retrospective Compilation Rationale

## 1. Problem Statement
Retrospectives are critical to **SG-0005: Autonomous Knowledge Accrual**. However, manual collection of telemetry logs, node transitions, and API latencies introduces significant friction, violating **SG-0003: Preservation of Autonomous Velocity**.
Furthermore, manual summaries suffer from human recall bias, selective filtering of errors, and the normalization of deviance.

## 2. Rationale for the Hybrid Model
To solve this, we separate the compilation into two phases:
- **Deterministic compilation**: The compiler extracts facts directly from `telemetry.jsonl` and `frontier_state.yml` to guarantee 100% accuracy and repeatability.
- **Agentic inference**: The agent uses local LLM reasoning to infer the 5 Whys and action items. This keeps the execution entirely offline (preserving autonomous velocity) while utilizing the agent's reasoning capability.

## 3. Rationale for Aristotelian Causality Framing
By structuring the input according to the Four Causes, we provide a mathematically and philosophically rigorous interface for the operator:
- The operator defines the **Formal** and **Final** causes (design templates and goals).
- The system manages the **Material** and **Efficient** causes (raw telemetry data and execution parsing).

This boundary prevents conversational fatigue (**SG-0004**) while maintaining high-fidelity alignment.
