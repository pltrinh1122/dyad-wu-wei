#!/bin/bash
SPAO_PERSONA_ID=agent-ziran ./bin/node cancel 1507 "Path: Remediate stale audit_state.json survivor" "Redundant Path; execution bypassed and completed via Activity 1511 directly"
SPAO_PERSONA_ID=agent-ziran ./bin/node cancel 1503 "Path: [BUG] Intake: System Crash in sync" "Redundant bug duplicate; root cause remediated via Path 1511"
SPAO_PERSONA_ID=agent-ziran ./bin/node cancel 1498 "Path: [BUG] Intake: System Crash in reflect" "Redundant bug duplicate; root cause remediated via Path 1511"
SPAO_PERSONA_ID=agent-ziran ./bin/node cancel 1423 "Path 1423: Codify Redundant Node Closure Discipline" "Path execution completed; final retrospective synthesized in retro-1423-final.md but node remained open in Github"
