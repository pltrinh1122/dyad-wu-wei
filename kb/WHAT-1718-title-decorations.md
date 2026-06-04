# WHAT-1718: Falsify Title Decorations

## Goal
Remove `Node` and `Activity` prefixes from issue titles, local ledgers, and templates as they are no longer necessary for operator monitoring and create redundancy in the topological map.

## Context
Historically, issues were prepended with `Node <ID>:` or `Activity <ID>:` to help Operators distinguish between different topological units in GitHub. With the advent of `bin/status`, `bin/backlog view`, and the DAG visualization tools, these prefixes have become vestigial text that merely clutters the UI and causes synchronization anomalies.

## Invariants Formulated
1. **Title Purity Invariant**: All CLI tools and internal synchronization mechanisms MUST NOT prepend `Node <ID>:` or `Activity:` to GitHub issue titles or local `frontier_state.yml` identifiers. 
2. **Backward Compatibility Parsing Invariant**: The Agentic State Machine (e.g. `daemon_nba.py`) MUST fall back to parsing `#(ID)` from the local ledger if the literal word `Node` is missing, ensuring backward compatibility with both legacy formats and the new pure ID formatting.

## Changes Made
- Modified `kernel/agent_frontier.py` to format active nodes as `#{id}: {title}` instead of `Node {id}: {title}`.
- Modified `kernel/daemon_backlog.py` to drop `Node` when formatting the Meta-Index, utilizing `#{id}: {title}` instead.
- Modified `kernel/daemon_node.py` to correctly parse and format without `Node` prefix.
- Modified `kernel/daemon_knowledge_accrual.py` to remove `Node {id}:` prefix dependencies.
- Updated `daemon_nba.py` regex `match = re.search(r"(?:Node |#)(\d+)", n_name)` to gracefully handle both old and new formats.
- Fixed associated tests in `tests/test_frontier_editor.py` and `tests/test_daemon_backlog.py`.
