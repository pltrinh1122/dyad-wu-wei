# High-Reliability Agentic Retrospective (SHAR) - {assessment_title}

## 1. Executive Abstract
- *3-sentence synthesis*: (1) What occurred, (2) the core technical/procedural lesson, and (3) the primary systemic recommendation.

## 2. Operational Metrics & Timeline
| Metric | Baseline | Observed | Variance |
| :--- | :--- | :--- | :--- |
| Execution Time (Avg/Node) | | | |
| GitHub API Latency (Avg) | | | |
| Active Worktrees / Local Size | | | |
| Duplicate File Lock Contention | | | |

- **Milestone Timeline**:
  - {timeline_events}

## 3. Anomaly Classification Taxonomy (ACT) Log
- **Tier 1: Mishaps (Actual Failures)**:
  - {tier1_mishaps}
- **Tier 2: Close Calls (Latent Gaps)**:
  - {tier2_close_calls}
- **Tier 3: Precursors (Weak Signals / Mundane Seeds)**:
  - {tier3_precursors}
- **Tier 4: Calibrations (Benign Variance / False Alarms)**:
  - {tier4_calibrations}

## 4. Root Cause Analysis (RCA) - The 5 Whys
- **RCA-0001**: {rca_title}
  1. *Why?* {why1}
  2. *Why?* {why2}
  3. *Why?* {why3}
  4. *Why?* {why4}
  5. *Why?* {why5}

## 5. Corrective Action Matrix
- **Preventative Actions**:
  - [ ] {preventative_tasks} (Traces to RCA-000X)
- **Mitigation Actions**:
  - [ ] {mitigation_tasks} (Traces to RCA-000X)

## 6. Closed-Loop Policy Infusion
- **Rule/Template Updates**: {kb_mutations}
- **Code/Guardrail Updates**: {orchestrator_updates}

---

## 7. Falsifiable Conditions of the SHAR Framework
*Note: If any of these conditions are met, the SHAR Framework must be declared falsified/defective, and user/operator alignment must be initiated to redesign the loop.*

1. **Precursor Blindness (False Negatives)**: A Tier 1 Mishap (system rollback/halt) occurs, but the previous 3 telemetry runs recorded 0 Tier 2 (Close Calls) or Tier 3 (Precursors) warnings related to that domain.
2. **Alert Fatigue (False Positives)**: Tier 4 Calibrations constitute >50% of all logged anomalies over a 3-cycle moving average, indicating the telemetry rules are too noisy and drag down velocity.
3. **Knowledge Leakage (Infectious Regression)**: A Tier 1 or Tier 2 anomaly of the same technical root cause recurs within 2 sessions *after* a Section 6 policy update was committed to prevent it.
4. **Overhead / Velocity Drag**: The overhead of conducting the SHAR retrospective, compiling telemetry, and maintaining the ACT log consumes >15% of the agent's total session resource/token budget.
