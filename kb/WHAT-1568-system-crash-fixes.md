# WHAT-1568: Harmonize System Crash Fixes

## 1. Intent
System crashes that interrupt the autonomous execution loop introduce friction and block the Wu-wei Dao. This document harmonizes the resolutions for a series of system crashes (Path 1567) to ensure they are codified as system invariants.

## 2. Resolved Vulnerabilities

### A. Git Switch Conflicts (Node 1531)
* **Crash:** The `sync` command crashed when `git switch` encountered detached or conflicting local branches during branch transitions.
* **Resolution:** Handling git switch errors gracefully in `sync_and_clean_node` and merging duplicate switch definitions in `git_client.py`. 

### B. Prompt Daemon Initialization (Node 1572)
* **Crash:** `daemon_prompt.py` crashed when trying to append to an incorrectly initialized dictionary type instead of a list.
* **Resolution:** Re-initialized prompts as lists, fixing the dictionary append crash.

### C. Validation Gate Escapes (Node 1579)
* **Crash:** Validation gates were throwing unhandled exceptions that crashed the kernel_daemon abruptly.
* **Resolution:** Refactored validation gates to use `sys.exit(2)` (or equivalent) for clean operational failure handling instead of raw exceptions.

### D. GitHub GraphQL Deprecation Noise (Node 1641)
* **Crash:** GitHub CLI emitted GraphQL deprecation warnings on `stderr`, causing `gh issue view` to exit with status 1. This broke `daemon_nba.py` and surfaced corrupt mock nodes.
* **Resolution:** Handled stderr parsing safely and accounted for deprecation warnings without triggering a hard failure.

## 3. Feedforward Invariants
1. **Validation Gate Exit**: All future validation gates must cleanly exit the process rather than raising unhandled exceptions.
2. **Subprocess Resilience**: External CLI integrations (like `gh` and `git`) must handle `stderr` noise resiliently without seizing the execution loop.
