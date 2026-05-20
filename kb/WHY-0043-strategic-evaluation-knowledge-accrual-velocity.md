# WHY-0043: Strategic Evaluation — Knowledge Accrual Pipeline vs Offline Velocity Priority

## Context & Problem Statement
As we scale the metarepository towards full autonomy, we face a strategic tradeoff between two core strategic goals:
1. **SG-0005 (Autonomous Knowledge Accrual)**: Bootstrapping pipelines for automatic memory construction, KDR indexing, and topological tracing.
2. **SG-0003 (Preservation of Autonomous Inner-Loop Velocity)**: Hardening the local test suite to ensure 100% offline hermetic execution and sub-second test execution speeds.

We must define a formal framework to resolve whether knowledge accrual pipelines or offline velocity remediation should be prioritized first.

## Decision
We prioritize the **Offline Velocity Baseline** (SG-0003, Path 368) over **Autonomous Knowledge Accrual** (SG-0005) when local testing relies on live network resources or exceeds acceptable execution latency thresholds.

### Rationale
1. **Hermeticity is the Platform**: Knowledge accrual pipelines and auto-indexing scripts must execute code generators, run tests, and validate state changes. If the underlying test execution environment relies on live external resources, any automated pipeline will suffer from network flakiness, rate-limiting, and non-deterministic failures.
2. **Compound Execution Speed**: The velocity of the local test runner directly determines the speed at which an agent can iterate, debug, and learn. Prioritizing offline velocity ensures that all downstream autonomous knowledge indexing and validation loops execute in milliseconds instead of seconds, compounding our engineering leverage.
3. **Safety and Containment**: Autonomous agents cannot safely compile or index knowledge without a fully sandboxed and isolated local test environment. Eliminating live network calls guarantees that the agent's inner-loop is strictly contained and hermetic.

## Strategic Invariants
- **Hermeticity Prerequisite**: Establishing a 100% offline and network-isolated local environment is a hard prerequisite before launching any automated knowledge accrual or indexing pipelines.
- **Velocity Threshold Gate**: If the unit test suite fails a hermetic audit or has latency above the acceptable threshold, all resources must switch to velocity remediation before any new knowledge-accrual tasks are activated.
