# WHAT-0043: Strategic Evaluation — Tradeoff Matrix & Prioritization Logic

## Tradeoff Matrix
To decide between bootstrapping the Autonomous Knowledge Accrual Pipeline and preserving Offline Velocity, the system evaluates backlog items against the following dimensions:

| Dimension | Autonomous Knowledge Accrual (SG-0005) | Offline Velocity Baseline (SG-0003) | Prioritized Path |
| :--- | :--- | :--- | :--- |
| **Execution Dependency** | Relies on the test suite to validate state changes and knowledge correctness. | Self-contained, isolated local test environment. | Velocity Baseline |
| **Pipeline Stability** | Subject to flakiness and timeouts if external network dependencies exist. | Deterministic, offline, hermetic unit tests. | Velocity Baseline |
| **Compounding Acceleration** | Adds automation loops that run downstream of the developer inner-loop. | Accelerates the primary developer/agent inner-loop itself. | Velocity Baseline |
| **Containment Assurance** | None (Runs wide-ranging analytical searches). | High (Strictly isolates execution from the public internet). | Velocity Baseline |

## Technical Rules & Prioritization Logic

1. **Velocity Baseline Rule**: Prioritizing the offline velocity baseline (SG-0003, Path 368) is a hard prerequisite for any path under SG-0005 (Autonomous Knowledge Accrual). 
2. **Prioritization Gate**:
   - The strategic manager automatically ranks `Velocity` baseline paths (SG-0003) above any `Knowledge Accrual` paths (SG-0005) if:
     - The metasystem audit detects live network calls or unmocked API endpoints in the test suite.
     - Unit test execution latency exceeds `2.0` seconds on local runs.

## Verification & Status
- **Status**: Locked and Verified
- **Verified by**: Node 426 Plan Probe & Node 427 Reflect Activity
