# Discovery: Gut Local Lock Ledger and Implement API-Driven kernel_daemon for Swarm Fan-Out

## 1. Intent Formulation
The system previously utilized a global, monolithic Git-tracked ledger (`artifacts/frontier_state.md` and `.yml`) to enforce the `WIP-N=1` invariant across the entire repository. This centralized lock mathematically prevented true swarm fan-out. Because `plan-start` and `reflect` synchronously updated the same physical lockfile on `main`, invoking multiple sub-agents resulted in inescapable Git push collisions. 

## 2. Dialectical Realization
The `WIP-N=1` constraint is designed to protect **cognitive focus** (the context window of the Agent, and the working memory of the Operator). Therefore, the invariant targets the *Persona*, not the *Repository*. A repository can safely host N=100 isolated `.worktrees/`. 
Applying a global N=1 lock to the entire physical repository was a category error that broke concurrency.

## 3. Structural Decision
We must implement **The Cloud Ledger (Approach C)**:
- **Locking:** `plan-start` and `reflect` will no longer modify the `frontier_state` files tracked in Git to acquire execution locks. The true Execution Lock is defined by the GitHub DAG (`status: active` label).
- **The Ad-Hoc kernel_daemon Ledger:** `bin/status` will no longer parse a static `.yml` lockfile. Instead, it will dynamically query the GitHub API to render a real-time table of which persona holds which active node.

## 4. Next Actions
- [x] Create Plan node.
- [ ] Refactor `kernel/node_lifecycle.py` and `kernel/agent_frontier.py` to strip the physical Git-lock mechanisms.
- [ ] Refactor `bin/status` to render the ad-hoc API ledger.
