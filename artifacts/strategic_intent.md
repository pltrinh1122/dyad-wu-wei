# Strategic Intent Ledger

## Active Goals
### NS-0001: Operational Leverage through Autonomous Reliability (North Star)
- **Operator Problem**: The operator suffers from attention overhead and context-switching fatigue when guiding autonomous agents, preventing scale.
- **Constraints**: The system must operate under real-time session limits, operator attention boundaries, and standard repository rules.
- **Falsification Signal**: The ratio of operator attention time (conversation, reviews, debug gates) to completed backlog nodes increases over a 30-day window.
- **Prioritized Paths**: None

### SG-0001: Backlog Dynamics and Resource Budget Alignment
- **Operator Problem**: The system wastes computational resources and LLM token budgets executing low-impact paths because backlog selection and path execution are decoupled from active strategic policies.
- **Constraints**: Backlog prioritization must be evaluated deterministically during the SENSE phase using active ledger goals.
- **Falsification Signal**: The agent spends resource/token budget on paths that are not prioritized in the strategic ledger.
- **Prioritized Paths**: 404

### SG-0002: Gateless Autonomous Execution within Risk-Managed Sandbox
- **Operator Problem**: The agent cannot execute autonomously because the lack of automated network egress isolation, process containment, and transaction rollback mechanics poses an unacceptable risk of codebase or workspace corruption.
- **Constraints**: The sandbox must enforce hard CPU/memory limits, restrict network egress to an allowlist, and guarantee idempotent git tree state rollbacks.
- **Falsification Signal**: The operator re-introduces manual human-in-the-loop review gates because the sandbox policies fail to isolate or rollback unsafe mutations.
- **Prioritized Paths**: None

### SG-0003: Preservation of Autonomous Velocity
- **Operator Problem**: Autonomous agent velocity is degraded because non-deterministic (flaky) tests or slow validation runs trigger false-positive auto-rollbacks, stalling the agent in repeating repair loops.
- **Constraints**: Validation test suites must execute completely offline, contain zero network dependencies, and run in under 60 seconds.
- **Falsification Signal**: The agent's throughput (nodes completed per unit of time) decreases due to repeating rollback cycles caused by test flakiness or network timeouts.
- **Prioritized Paths**: 368

### SG-0004: Efficient Intent-to-Goal Policy Communication
- **Operator Problem**: Defining strategic goals and aligning on technical designs requires verbose, high-overhead conversational alignment loops, leading to operator decision fatigue.
- **Constraints**: Intent must be communicated exclusively through structured policy definitions (strategic_intent.yml) with falsifiable metrics.
- **Falsification Signal**: The operator spends more than 10% of their session time in interactive conversational turns rather than simple policy updates.
- **Prioritized Paths**: None

### SG-0005: Autonomous Knowledge Accrual
- **Operator Problem**: The human attention required to guide the agent remains static because the agent cannot autonomously capture, codify, and apply lessons from its execution failures to future plans.
- **Constraints**: Knowledge mutations under the kb/ directory must be verified for structural validity and must not violate immutable core axioms.
- **Falsification Signal**: The average number of agent repair cycles on repeat error patterns does not decrease over subsequent sessions targeting the same domain.
- **Prioritized Paths**: None

## Draft Goals
*No goals in this state.*

## Achieved Goals
*No goals in this state.*

## Falsified Goals
*No goals in this state.*
