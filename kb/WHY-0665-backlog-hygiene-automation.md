# WHY-0665: Automate Backlog Hygiene via Python Governance Rules

## Decision
We affirm the architectural invariant that **Backlog Hygiene must be maintained via deterministic Python governance rules** rather than LLM agent sweeps. If an LLM agent is required to manually sweep a backlog to maintain hygiene, the system's automation design has failed.

## Context
Path 664 challenges the notion that the agent should be responsible for finding orphaned nodes, closing stale issues, or manually aligning the backlog. In a highly capable autonomous system, the Engine itself (via `daemon_nba.py`, `daemon_status.py`, and GitHub actions/hooks) should enforce hygiene.

## Rationale
1. **Determinism over Inference:** Backlog state is a topological graph. Evaluating graphs is a deterministic computer science problem ($O(1)$ to $O(N)$), not an open-ended inference task. Utilizing token-based LLM inferences for graph traversal is an anti-pattern that leads to Agentic Seizures.
2. **Recent Evidence:** In earlier sessions, a bug in `daemon_nba.py` caused the system to fetch orphaned backlog items due to a pagination truncation bug and an N+1 API call timeout. Attempting to have the agent "manually sweep" these items resulted in infinite loops. By patching the underlying Python Engine to use $O(1)$ body parsing, the system inherently ignored orphaned nodes and automatically acquired the correct active Path priority.

## Consequences
- **The LLM Agent is formally relieved** of any responsibility to "sweep" or "clean up" the backlog.
- Any future hygiene issues (e.g., orphaned nodes, incorrect statuses) MUST be treated as bugs in the Python Orchestrator (`orchestrator/mgr_backlog.py`, `kernel/daemon_nba.py`) and patched in the codebase.
- We will NOT create a "Janitor" persona or agent to manage the backlog.
