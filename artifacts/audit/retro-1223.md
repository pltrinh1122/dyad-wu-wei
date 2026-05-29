# Retrospective: triage label naming deviation (retro-1223)

## Timeline & Detection
- **2026-05-27 18:52**: The Agent implemented the Quarantine Protocol using the label `triage` based on the intake requirement prompt.
- **2026-05-27 19:12**: The Operator reported that the Healer expected the status-prefixed label `status:triage` instead of the bare `triage` label to maintain consistency with the repository's ontology.

## Root Cause
The initial implementation used the label `triage` literally as requested, which deviated from the standard status-prefix ontology (e.g. `status:active`, `status:backlog`) used by the metasystem status check and other lifecycle triggers.

## Codified Insight
All status-related labels representing quarantine or lifecycle phases (like triage) must strictly use the `status:` namespace prefix (e.g., `status:triage`) to ensure seamless integration with systemic audits.
