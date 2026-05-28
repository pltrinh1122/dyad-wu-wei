# WHAT-0042: Value Comparison — Evaluation Framework

## Evaluation Matrix
To decide between Speculative Gap Analysis and Immediate Velocity Remediation, the system evaluates backlog items against four key dimensions:

| Dimension | Speculative Gap Analysis | Immediate Velocity Remediation | Priority Recommendation |
| :--- | :--- | :--- | :--- |
| **Certainty of Gain** | Low (Theoretical gaps may never materialize) | High (Direct reduction in test suite runtime / flaky failures) | Velocity Remediation |
| **Compounding Speed** | Linear (Informs future design documents) | Exponential (Speeds up all future execution runs) | Velocity Remediation |
| **Risk of Waste** | High (Analysis paralysis or over-engineering) | Negligible (Improving code quality / isolation always pays off) | Velocity Remediation |
| **Hermeticity Guard** | Indirect (Identifies missing boundaries) | Direct (Remediates and closes live network connections) | Velocity Remediation |

## Technical Rules & Prioritization Logic

1. **The Velocity Threshold**: If the local test execution speed exceeds `2.0` seconds or if the suite relies on external network connections, any pending "Velocity Remediation" path must be prioritized before starting new feature/gap discoveries.
2. **Deterministic Backlog Sorter**:
   - Classify all backlog paths as either `Velocity` or `Speculative`.
   - The strategic manager automatically ranks `Velocity` paths higher than `Speculative` paths in the Next-Best-Action recommendation queue if the test suite fails the hermetic audit.
