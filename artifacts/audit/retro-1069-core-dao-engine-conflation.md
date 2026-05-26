# Retrospective: Semantic Drift and Conflation of "Core" and "Dao Engine"

## Context
During the PR #1132 review (Node 1069), the Operator proposed the thesis that the terms "Core" and "Dao Engine" are being conflated across our artifacts. The Agent was instructed to falsify this thesis.

## Violation
Upon inspection of the `kb/` primitives, the Agent discovered that the thesis is true and cannot be falsified. The knowledge base contains explicit semantic conflations, such as in `HOW-0935-isbo-protocol.md`: 
`"2. Clone the core Dao Engine repository to a designated engine path:"`

This phrase erroneously merges the static machinery (`Core`) with the materialized continuous inference loop (`Dao Engine`). This semantic drift violates the strict ontological precision required by the Dao-Ziran architecture.

## Codified Insight
Because the thesis aligns with the observable state of the repository, it cannot be falsified. The Agent formally concedes that the artifacts are suffering from semantic drift. A sweeping lexical audit is required to purge the term "Core Dao Engine" and enforce the strict boundary:
- **Core**: The static, cloned repository of orchestrators and tools (`SPAO_CORE_DIR`).
- **Dao Engine**: The living, materialized cybernetic loop that requires Compute, Storage, a Sovereign Domain (`kb/`), and Semantic Entropy (LLM).

## Resolution
The Agent has codified this semantic violation into this retrospective. Because the SPAO loop is currently locked by PR #1132 (WIP-N=1), a full lexical refactor of the `kb/` cannot be executed immediately. A prompt has been queued to execute this systematic scrub as a distinct Backlog Node once the merge gate is lifted.
