# WHAT-0916: Status Report Progress Bars & Goal Ratios Specification

## Classification
- **Type**: WHAT (Specification)
- **ID**: WHAT-0916
- **Author**: agent-ziran
- **Created**: 2026-05-28 (Node 918, Path 916)
- **Status**: Draft

---

## 1. Goal

Enhance the status reporting system to display visual progress bars and tactical completion ratios mapped to active Strategic Goals, reducing Operator cognitive load.

---

## 2. Technical Specification

### 2.1 Progress Calculation Logic

For each active Strategic Goal defined in `artifacts/strategic_intent.yml`:
1. Retrieve the list of `prioritized_paths`.
2. Retrieve the list of all open issues using `drivers.github_client.get_open_issues()`.
3. A prioritized path is defined as **Completed** if its ID is not present in the open issues list.
4. Calculate the Completion Ratio:
   - If the total number of prioritized paths is 0, the ratio is `1.0` (100%).
   - Otherwise, the ratio is `completed_paths / total_prioritized_paths`.

### 2.2 Progress Bar Rendering

The status CLI adapter (`bin/status`) will render each active Strategic Goal with its progress:
1. Render the Strategic Goal header with its ID and title (e.g. `🎯 [SG-0004] Efficient Intent-to-Goal Policy Communication`).
2. Render an ASCII progress bar using:
   - Solid block characters (`█`) for the completed portion.
   - Light shade block characters (`░`) for the remaining portion.
   - Total bar width of 10 characters (each block representing 10% progress).
3. Append the numerical completion percentage and fraction (e.g., `[█████░░░░░] 50.0% (2/4)`).
4. List the status of each prioritized path under the goal:
   - Completed paths: `[x] Path <id>: <title>`
   - Open paths: `[ ] Path <id>: <title>`

### 2.3 Command Line Interface Output

The visual progress report will be printed directly below the general system status section when executing `./bin/status`.

---

## 3. Verification Plan

### 3.1 Unit Testing
- Test calculation logic with mock strategic intent ledgers and mock open issues.
- Verify progress bar formatting for 0%, 50%, and 100% scenarios.
- Verify fallback behavior when there are 0 prioritized paths.
