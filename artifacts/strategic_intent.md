# Strategic Intent Ledger

## Active Goals
### SG-0001: SPAO Prioritization and Backlog Governance
- **Operator Problem**: The operator has low visibility into the urgency and priority of probes/paths, causing cognitive load and backlog stagnation because broader strategic intent is not tracked and enforced.
- **Constraints**: The system operates under existing repository structures, GitHub API limits, and a dual-probe initialization pattern.
- **Falsification Signal**: The operator manually overrides Next-Best-Action recommendations consistently even after intent prioritization is active.
- **Prioritized Paths**: 404

### SG-0002: Gateless Autonomous Execution within Risk-Managed Sandbox
- **Operator Problem**: Binary gates (PR review gates, SENSE-phase gates) require high manual oversight, causing cognitive load, context-switching fatigue, and system stagnation.
- **Constraints**: The system operates under git tree transactions, virtual environment sandboxes, and API/token consumption limits.
- **Falsification Signal**: The operator re-introduces manual approval gates to prevent damage because the sandbox policies fail to isolate or rollback unsafe mutations.
- **Prioritized Paths**: None

### SG-0003: Preservation of Autonomous Velocity
- **Operator Problem**: Fragile testing infrastructure and flaky/non-deterministic tests trigger false-positive auto-rollbacks, which stalls the agent's progress and requires manual intervention.
- **Constraints**: Tests must run offline without making live network calls and must execute in under 60 seconds.
- **Falsification Signal**: The agent's autonomous throughput (nodes completed per hour) decreases due to repeating rollback loops caused by unresolved test flakiness.
- **Prioritized Paths**: 368

### SG-0004: Efficient Intent-to-Goal Policy Communication
- **Operator Problem**: Defining strategic goals and aligning on technical designs requires verbose, high-overhead conversational alignment loops, leading to operator decision fatigue.
- **Constraints**: Goals must be expressed in a structured format (strategic_intent.yml) using falsifiable metrics.
- **Falsification Signal**: The operator spending more than 10% of their session time in interactive alignment discussions rather than simple policy updates.
- **Prioritized Paths**: None

## Draft Goals
*No goals in this state.*

## Achieved Goals
*No goals in this state.*

## Falsified Goals
*No goals in this state.*
