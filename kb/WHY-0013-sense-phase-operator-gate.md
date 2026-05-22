# WHY-0013: Sense-Phase Operator Gating

## 1. Context
Antigravity agents are designed to execute the SPAO (Sense-Plan-Act-Observe) loop autonomously. As the Frontier Agent, the agent reads the topological state, consults the `nba_evaluator`, and sequentially processes Nodes from the backlog.

However, a fundamental architectural flaw was observed: agents consistently execute `bin/node sync` (Sense phase), observe the `Next-Best-Action` output, and autonomously jump straight into `bin/node plan-start` (Plan phase). This creates a runaway train effect, stripping the human operator of the ability to re-prioritize, pause execution, or seamlessly switch Paths without forcibly interrupting the agent mid-plan.

## 2. Decision
To restore strict operational control, we are implementing a **Two-Pronged Sense-Gate**:
1. **The Behavioral Gate (Meta-Instruction Invariant)**: We mathematically forbid SENSE -> PLAN transitions without explicit operator alignment.
2. **The Environmental Gate (Visual Cue)**: We inject an inescapable ANSI-colored blocker string directly into the output of the Next-Best-Action evaluator to physically halt the agent's contextual momentum.

## 3. Rationale
Relying purely on behavioral prompts (e.g., telling the LLM "don't do this") is brittle due to the inherent eagerness of LLMs to "complete the task" when presented with a clear `Next-Best-Action`. By combining a formal Meta-Instruction invariant in `GEMINI.md` with an overwhelming environmental warning in the CLI output, we break the agent's contextual momentum. The agent reads the massive `🛑` warning, recognizes the invariant trigger, and naturally halts to query the operator.

## 4. Consequences
- **Positive**: Complete operator control over the cadence of execution. The repository will never advance to a new Node without the operator explicitly invoking or approving the transition.
- **Positive**: Better adherence to the `WIP-N=1` invariant by ensuring parallel or runaway executions are gated at the lowest common denominator (the Sense phase).
- **Negative**: Agents will require explicit chat-interface confirmation after every Node completion, slightly increasing the operator's manual overhead (a desired trade-off for safety).
