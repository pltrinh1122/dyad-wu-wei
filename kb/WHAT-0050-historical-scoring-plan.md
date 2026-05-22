# WHAT-0050: Historical Path Scoring Plan

This document defines the execution strategy and reporting format for Next-Best-Action (NBA) scoring across historical paths.

## 1. Scope of Scored Paths

The scoring engine will evaluate all paths within a range specified by the user. If no range is specified:
* It defaults to scoring all Path issues currently active or open in the repository backlog.

## 2. CLI Interface Design

A new option will be added to the runtime CLI helper (`./bin/rt` or `kernel/mgr_rt.py`):
```bash
./bin/rt score-paths --start <ID> --end <ID>
```

Parameters:
* `--start <ID>`: The starting issue/path ID (inclusive).
* `--end <ID>`: The ending issue/path ID (inclusive).

If parameters are omitted, the script dynamically retrieves all open Path issues.

## 3. Reporting Structure

The output will be formatted as a structured report:
1. **Header**: Methodology reference, mapping back to the mathematical scoring rubric defined in `kb/WHAT-0048-nba-scoring-rubric.md`.
2. **Scored Entries**: A table displaying:
   * Path ID & Title
   * Overall Score
   * Individual component addends: Dependency ($C_{\text{Dependency}}$), Axiomatic compliance ($C_{\text{Axiom}}$), Strategic Alignment ($C_{\text{Strategic}}$), Operational Risk ($C_{\text{Risk}}$).
3. **Summary**: The total sum of scores of all evaluated paths.
