# WHAT-0064: Persona-Aware Soft-Routing (NBA Filtering)

## Purpose
This specification defines the structural mechanism for the Next-Best-Action (NBA) Scorer to soft-route execution paths based on the active agent persona. This prevents domain collisions and execution deadlocks by gracefully filtering out paths that the running agent is not authorized to execute.

## Specification

### 1. Persona Detection
The active persona identity MUST be retrieved deterministically using the following order of precedence:
1. `SPAO_PERSONA_ID` environment variable (if present).
2. `agent_id` parameter inside `antigravity.yml` (fallback).

### 2. Ownership Resolution
The NBA scorer MUST resolve path ownership by tracing the candidate node back to its parent `Strategic Goal (SG)` using the `artifacts/strategic_intent.yml` ledger. The SG ID is then mapped to the authorized persona via the immutable `kb/WHAT-0062-agent-persona-ownership-index.md` index.

### 3. Scoring Matrix (c_persona)
A `c_persona` boolean modifier is introduced to the NBA scoring formula:
- If `WHAT-0062` is **present** and the active persona **matches** the path's owner, `c_persona = 1.0`.
- If `WHAT-0062` is **present** and the active persona **does not match** the path's owner, `c_persona = 0.0` (Soft-Routed).
- If `WHAT-0062` is **absent** (e.g., during bootstrapping or parallel agent execution), `c_persona = 1.0` (Fail-Open).

### 4. Mathematical Integration
The final scoring formula is updated to strictly enforce the modifier:
`S_NBA = C_dep * C_persona * (0.40 * C_axiom + 0.40 * C_strategic + 0.20 * C_risk)`

## Compliance
- Implementations MUST use TDD mocks in `tests/test_nba_scorer.py` to assert the correct behavior of the fail-open and fail-closed logic without requiring the physical presence of `WHAT-0062` during testing.
