# WHAT-1915: Implementation Plan for SG-0008

## 1. Intent
To formalize the technical implementation of SG-0008, established in WHAT-1914, to ensure exogenous support requirements are routed and metabolized without corrupting the NBA Scorer.

## 2. Implementation Steps
1. **Strategic Ledger Update**: 
   - Modify `artifacts/strategic_intent.yml` to insert `SG-0008: Metasystem Operational Integrity & Support Triage` with `priority: 2`.
   - Ensure the new SG sits just below the primary onboarding or critical operational SGs to intercept unmapped support tickets.

2. **Path Re-Mapping**:
   - Update `Path 1913: Path: Triage Holding & External Intakes` to belong to `SG-0008`.
   - Update `Path 1926: Path: [BUG] Intake: System Crash in sync` to belong to `SG-0008`.
   - Update any remaining closed paths mapped incorrectly in the strategic ledger.

3. **CSI Guards Integration**:
   - Verify `daemon_nba.py` handles the new SG priority properly. (Already validated theoretically).
