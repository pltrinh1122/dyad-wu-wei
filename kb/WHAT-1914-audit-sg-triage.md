# WHAT-1914: AUDIT SG and Triage Holding

## 1. Intent
To formally define the cybernetic routing mechanism for exogenous `[SUPPORT]` tickets, bug reports, and external requirement intakes without violating the NBA Scorer's algorithmic reliance on the Strategic Intent Ledger.

## 2. The Problem: Starvation of Unmapped Intakes
Because `daemon_nba.py` rigorously prioritizes backlog issues according to `artifacts/strategic_intent.yml`, any issue that does not belong to a prioritized Path/SG is relegated to the `unmatched_items` pool. This causes critical operational interrupts (e.g., system crashes or dyadic support tickets) to be completely starved at the bottom of the queue until all active SGs are 100% completed.

## 3. The Resolution: SG-0008 Operational Integrity
Instead of writing brittle "interrupt logic" or hardcoding `[SUPPORT]` label overrides into the Python engine, we solve the problem topologically.
We will introduce a dedicated Strategic Goal: **`SG-0008: Metasystem Operational Integrity & Support Triage`**.

### Mechanics:
1. **Topological Purity**: `SG-0008` is placed at the top of the Strategic Intent Ledger (just beneath the North Star). This grants it perpetual maximum priority.
2. **Quarantine Preserved**: Incoming `[SUPPORT]` issues land in the `[Backlog / Unmapped]` bucket (Quarantine). They do not hijack the engine automatically.
3. **The Sluice Gate Pull**: The Operator evaluates the quarantined issue and formally maps it to a standing Path (e.g., `Path: Triage Holding & External Intakes`) underneath `SG-0008`.
4. **Immediate Metabolism**: Once mapped, the Engine's unmodified NBA Scorer naturally elevates the issue to the Next-Best-Action because its parent SG is Priority 1.

## 4. Required Implementation Steps (For Node 1915)
- Update `artifacts/strategic_intent.yml` to inject `SG-0008: Metasystem Operational Integrity & Support Triage`.
- Instantiate a standing Path issue on GitHub (e.g., `Path: Triage Holding & External Intakes`) and map it to `SG-0008`.
- Remap existing bug-fix or triage Paths (e.g., Path 1547, Path 1242) from SG-0006 or SG-0003 into SG-0008 to clean up the ledger taxonomy.
