## Goal
Execute Friction Triage to reconcile the deprecated terms (`dao`, `ziran`, `align`) across the corpus to clear the execution seizure and restore test suite viability.

## Scope
1. **Sweep and Translate:** Identify instances of deprecated terms in active code/documentation and translate them to their active counterparts (`wu-wei`, `friction_triage`, `harmonize`).
2. **Immune-Zoning:** Identify legitimate legacy occurrences (e.g. historical retrospectives, test fixtures) and append them to `immune_zones` in `kb/semantic_ledger.yml` instead of modifying them.

## Constraints
- Do not modify historical audit files (`artifacts/audit/retro-*.md`); they must be immune-zoned.
- Ensure the `ziran_auditor.py` and its associated tests are updated or immune-zoned appropriately.
