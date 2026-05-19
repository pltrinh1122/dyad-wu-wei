# WHY-0016: NBA Promotion to First-Class Primitive

## Context
The `nba_evaluator.py` logic was initially implemented as a stateless **Skill**. However, as the system matured, this "Skill" began to encapsulate complex **Workflow** logic, including multi-tier navigation strategies (Path Continuation vs. Path Switching) and hardcoded user-interface invariants (The Sense-Gate Invariant). 

During Probe 243, it was identified that this misclassification creates tight coupling between low-level graph parsing and high-level orchestration, making the system difficult to port to other domains (e.g., `agent-travel`) or customize via configuration.

## Decision
1.  **Elevation to Manager**: Promote the core navigation logic to `orchestrator/mgr_nba.py`. This manager owns the lifecycle of "Sensing" and "Recommending" work.
2.  **Stateless Decomposition**: Decompose the logic into a pure **Skill** (`skills/gh_graph_skill.py`) that handles data retrieval and parsing, and a **Workflow** that handles decision-making.
3.  **Configurable Navigation Strategy**: Move navigation parameters (repository name, fallback strategies, and UI templates) into `antigravity.yml` and `kb/templates/`.

## Rationale
-   **Separation of Concerns**: The orchestrator should decide *what* to do; the skill should know *how* to get the data.
-   **Systemic Invariant Enforcement**: Centralizing NBA logic in a Manager ensures that the **Sense-Gate Invariant** is enforced consistently across all domains via the `HookManager`.
-   **Portability**: By removing hardcoded repository strings and specific GH Issue body assumptions from the orchestrator, we allow the navigation engine to be reused across different project structures.

## Consequences
-   The legacy `skills/nba_evaluator.py` will be decommissioned.
-   `orchestrator/sense_hooks.py` will transition from calling a skill to delegating to a specialized manager.
-   The "Sense-Gate" UI will become editable via the Knowledge Base.
