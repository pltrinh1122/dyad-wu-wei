# Strategic Intent Ledger

## Active Goals
### NS-0001: Synergistic Human-Agent Partnership (North Star - 1+1=3)
- **Collaborative Gap**: Unilateral automation hard-caps the system's output because the agent is limited by its local reasoning and the human is limited by manual review bandwidth.
- **Constraints**: The system must operate under real-time session limits, operator attention boundaries, and standard repository rules.
- **Falsification Signal**: The dyad fails to achieve greater throughput and architectural stability than the operator working alone or the agent executing without oversight.
- **Prioritized Paths**: None

### SG-0001: Backlog Dynamics and Resource Budget Alignment
- **Collaborative Gap**: The prioritization model fails to dynamically map the operator's high-level intent to the agent's backlog selection, causing attention drift between the partners.
- **Constraints**: Backlog prioritization must be evaluated deterministically during the SENSE phase using active ledger goals.
- **Falsification Signal**: The agent spends resource/token budget on paths that are not prioritized in the strategic ledger.
- **Prioritized Paths**: 299

### SG-0002: Gateless Autonomous Execution within Risk-Managed Sandbox
- **Collaborative Gap**: The human cannot safely delegate execution authority to the agent, creating a trust bottleneck where the human acts as a manual gatekeeper and the agent is blocked from executing autonomously.
- **Constraints**: The sandbox must enforce hard CPU/memory limits, restrict network egress to an allowlist, and guarantee idempotent git tree state rollbacks.
- **Falsification Signal**: The operator re-introduces manual human-in-the-loop review gates because the sandbox policies fail to isolate or rollback unsafe mutations.
- **Prioritized Paths**: 292, 532

### SG-0003: Preservation of Autonomous Velocity
- **Collaborative Gap**: Low-fidelity validation feedback (flaky or slow tests) breaks the agent's inner-loop verification, forcing the operator to intervene in tactical debugging rather than strategic governance.
- **Constraints**: Validation test suites must execute completely offline, contain zero network dependencies, and run in under 60 seconds.
- **Falsification Signal**: The agent's throughput (nodes completed per unit of time) decreases due to repeating rollback cycles caused by test flakiness or network timeouts.
- **Prioritized Paths**: None

### SG-0004: Efficient Intent-to-Goal Policy Communication
- **Collaborative Gap**: The communication interface requires verbose conversational turns instead of high-abstraction policy definitions, causing human decision fatigue and agent execution drift.
- **Constraints**: Intent must be communicated exclusively through structured policy definitions (strategic_intent.yml) with falsifiable metrics.
- **Falsification Signal**: The operator spends more than 10% of their session time in interactive conversational turns rather than simple policy updates.
- **Prioritized Paths**: None

### SG-0005: Autonomous Knowledge Accrual
- **Collaborative Gap**: The agent cannot autonomously codify and recall lessons from past failures, forcing the operator to repeatedly correct similar errors.
- **Constraints**: Knowledge mutations under the kb/ directory must be verified for structural validity and must not violate immutable core axioms.
- **Falsification Signal**: The average number of agent repair cycles on repeat error patterns does not decrease over subsequent sessions targeting the same domain.
- **Prioritized Paths**: 541

## Draft Goals
*No goals in this state.*

## Achieved Goals
*No goals in this state.*

## Falsified Goals
*No goals in this state.*
