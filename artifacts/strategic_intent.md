# Strategic Intent Ledger

## Active Goals
### NS-0001: Synergistic Human-Agent Partnership (North Star - 1+1=3)
- **Operator Problem**: Unilateral automation hard-caps the system's output at the limits of the agent's logic or the human's manual review bandwidth.
- **Constraints**: The system must operate under real-time session limits, operator attention boundaries, and standard repository rules.
- **Falsification Signal**: The dyad fails to achieve greater throughput and architectural stability than the operator working alone or the agent executing without oversight.
- **Prioritized Paths**: None

### SG-0001: Backlog Dynamics and Resource Budget Alignment
- **Operator Problem**: The system wastes resources and the operator suffers from decision fatigue because the backlog selection model fails to dynamically translate strategic intent into agent backlog sequencing, leaving execution decoupled from collaborative policies.
- **Constraints**: Backlog prioritization must be evaluated deterministically during the SENSE phase using active ledger goals.
- **Falsification Signal**: The agent spends resource/token budget on paths that are not prioritized in the strategic ledger.
- **Prioritized Paths**: 404

### SG-0002: Gateless Autonomous Execution within Risk-Managed Sandbox
- **Operator Problem**: The dyad cannot delegate execution authority because the lack of automated sandbox safety boundaries forces the operator to act as a manual execution gatekeeper, stalling autonomous velocity due to safety anxiety.
- **Constraints**: The sandbox must enforce hard CPU/memory limits, restrict network egress to an allowlist, and guarantee idempotent git tree state rollbacks.
- **Falsification Signal**: The operator re-introduces manual human-in-the-loop review gates because the sandbox policies fail to isolate or rollback unsafe mutations.
- **Prioritized Paths**: None

### SG-0003: Preservation of Autonomous Velocity
- **Operator Problem**: The collaborative velocity of the dyad is degraded because low-fidelity environmental feedback (flaky tests) triggers false rollbacks, dragging the operator back down to manual debugging and destroying trust in the agent's inner-loop verification.
- **Constraints**: Validation test suites must execute completely offline, contain zero network dependencies, and run in under 60 seconds.
- **Falsification Signal**: The agent's throughput (nodes completed per unit of time) decreases due to repeating rollback cycles caused by test flakiness or network timeouts.
- **Prioritized Paths**: 368

### SG-0004: Efficient Intent-to-Goal Policy Communication
- **Operator Problem**: The dyad fails to achieve high-level policy alignment because the communication interface requires verbose, low-abstraction conversational alignment loops, leading to operator decision fatigue and agent execution drift.
- **Constraints**: Intent must be communicated exclusively through structured policy definitions (strategic_intent.yml) with falsifiable metrics.
- **Falsification Signal**: The operator spends more than 10% of their session time in interactive conversational turns rather than simple policy updates.
- **Prioritized Paths**: None

### SG-0005: Autonomous Knowledge Accrual
- **Operator Problem**: The dyad's collective intelligence remains static because the agent cannot autonomously capture, codify, and apply lessons from its execution failures to future plans, forcing the operator to repeatedly correct the same error patterns.
- **Constraints**: Knowledge mutations under the kb/ directory must be verified for structural validity and must not violate immutable core axioms.
- **Falsification Signal**: The average number of agent repair cycles on repeat error patterns does not decrease over subsequent sessions targeting the same domain.
- **Prioritized Paths**: None

## Draft Goals
*No goals in this state.*

## Achieved Goals
*No goals in this state.*

## Falsified Goals
*No goals in this state.*
