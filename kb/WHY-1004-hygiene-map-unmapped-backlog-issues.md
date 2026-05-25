# WHY-1004: Hygiene Mapping for Unmapped Backlog Issues

## The Context
The Agent-Antigravity system relies on a rigid, formalized topological graph to prioritize work via the SENSE and Sluice Gate phases. All execution paths must be anchored to a Strategic Goal defined in the `artifacts/strategic_intent.yml` ledger (SG-0001: Backlog Dynamics and Resource Budget Alignment). 

As of Node 1004, the system identified four recent paths generated via direct chat interaction/hotfixes that exist in the global backlog but lack strategic mapping:
1. Path 1043: Codify Wu-wei NBA Handoff Message Structure
2. Path 1029: Fix Telemetry Logging Visibility
3. Path 1022: Refine DZ-CIL Intent Understanding
4. Path 1017: Codify Chat Immediacy Protocol

Failing to map these nodes violates the `WHAT-0038-strategic-goal-path-alignment-verification.md` invariant, causing hygiene warnings and degrading the Deterministic Scoring model's ability to prioritize them.

## The Alignment Strategy
To resolve this hygiene violation and restore full topological integrity, we must evaluate each unmapped node against the five core Strategic Goals (SG-0001 through SG-0005) and assign them to the most appropriate bucket.

### 1. Path 1043: Codify Wu-wei NBA Handoff Message Structure
- **Target SG:** **SG-0004 Efficient Intent-to-Goal Policy Communication**
- **Rationale:** This path enforces a deterministic, "Happy Path" recommendation structure that eliminates open-ended Agent questions. This directly targets the core metric of SG-0004: reducing Operator decision fatigue and minimizing conversational turns.

### 2. Path 1017: Codify Chat Immediacy Protocol
- **Target SG:** **SG-0004 Efficient Intent-to-Goal Policy Communication**
- **Rationale:** The Chat Immediacy Protocol ("Hai.") establishes a strict interaction boundary that prevents the Agent from engaging in unnecessary theoretical debates when receiving direct Operator commands, streamlining intent communication.

### 3. Path 1022: Refine DZ-CIL Intent Understanding
- **Target SG:** **SG-0004 Efficient Intent-to-Goal Policy Communication**
- **Rationale:** Accurate interpretation of Dao/Ziran/CIL intent prevents the Agent from misunderstanding Operator instructions, thereby reducing the need for clarifying conversational loops (the primary falsification signal for SG-0004).

### 4. Path 1029: Fix Telemetry Logging Visibility
- **Target SG:** **SG-0005 Autonomous Knowledge Accrual**
- **Rationale:** Telemetry visibility is the foundational prerequisite for the Agent's ability to passively audit its own execution history, diagnose systemic failures, and autonomously synthesize retroactive insights into the `kb/` without Operator intervention.

## The Materialization
The next phases (Plan/Act) will physically mutate `artifacts/strategic_intent.yml` to append these Path IDs (1043, 1017, 1022) to SG-0004, and Path 1029 to SG-0005.
