# WHAT-0666: Technical Design for Backlog Hygiene Automation

## Objective
To document the deterministic Python mechanisms that enforce Backlog Hygiene without requiring Agentic LLM inference, as aligned in `WHY-0665`.

## Implementation Details

The implementation relies on patching two critical daemons within the Manager Engine:

### 1. `kernel/daemon_status.py`
**Bug:** The status daemon was previously making paginated API calls that truncated the open issue list. When tracking issues, if an issue was pushed out of the first 30 (or 100) items of the default `gh issue list` view, the daemon erroneously concluded the issue was closed, leading to improper state assertions.
**Fix:** Refactored the underlying fetch to utilize `list_issues_by_label("path")` and `list_issues_by_label("backlog")` directly, ensuring that the full scope of relevant issues is loaded without arbitrary API pagination truncation.

### 2. `kernel/daemon_nba.py`
**Bug:** The Next-Best-Action (NBA) scorer suffered from an $O(N)$ API call anti-pattern where it fetched the details of every single open issue to determine its parent Path, causing timeout crashes and agentic seizures when faced with hundreds of unmapped orphaned nodes.
**Fix:** Refactored the NBA logic to utilize an $O(1)$ body regex parse. It now searches for `[x] Node {id}` within the bodies of prioritized `Path` issues to map children to paths. Orphaned nodes (nodes with no active Path) are automatically stripped of priority and demoted to the bottom of the list without requiring any LLM agent sweeping. 

## Falsification Protocol
- A backlog with 100+ "orphaned" nodes will not crash the NBA scorer.
- The Agent will not enter an infinite loop trying to manually sweep the backlog.
- `bin/node sync` will correctly ignore orphaned nodes and focus only on the children of prioritized Paths.

## Status
The implementation was completed synchronously alongside the architectural alignment in Node 665. The `daemon_nba.py` and `daemon_status.py` modules have been fully refactored, and all unit tests (including `test_daemon_strategic.py` and `test_daemon_status.py`) have been updated and are passing.
