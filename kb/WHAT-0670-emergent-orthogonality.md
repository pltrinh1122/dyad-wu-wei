# WHAT-0670: Technical Design for Emergent Orthogonality of Agent Scopes

## 1. Intent
To codify that orthogonality between agent scopes is not a top-down dictate from the `agent-meta` metasystem, but rather an emergent property of a decentralized contract system based on autonomous claims.

## 2. Theoretical Architecture
- **Meta Domain (The Chessboard)**: Owns the schema for declaring boundaries. `agent-meta` mandates that every agent must have a `WHAT-xxxx.md` manifest and defines the SPAOR rules that parse these manifests.
- **Individual Agents (The Players)**: Own the coordinates of their boundaries. They write their own claims to resources and code (e.g., `agent-platform` claims platform primitives, `agent-sg1` claims functional business logic).
- **Emergent Orthogonality**: The actual orthogonality is negotiated deterministically by the Next-Best-Action (NBA) scorer parsing overlapping or disjoint autonomous claims. 

## 3. Implementation Plan
1. Ensure that the `daemon_nba.py` (or `nba_scorer.py`) strictly respects agent identity (via `frontier_state.yml` and `agent-xxx` resolution) when scoring paths.
2. Ensure agents use `spao` primitives to declare their intended scope mathematically, rather than loosely in free-text.
3. Add tests to verify that `agent-meta` does not hardcode boundaries for `agent-platform`, but instead only reads the declared boundaries from the node/path structures.

## 4. Path Forward
This plan will be implemented in subsequent Activity nodes within Path 668.
