# WHY-0002: Linguistic Primitives over Semantic Jargon

**Date:** 2026-05-16
**Status:** Accepted

## Context
During the drafting of `INTAKE_BOOTSTRAP.md`, we identified a violation of "SPEC Orthogonality": the document blurred the lines between Definitions (the Ontology/What) and Instructions (the Spec/How). We evaluated splitting it into `KERNEL.md` and `OPERATING_PROTOCOL.md`, or `ONTOLOGY.md` and `INSTRUCTIONS.md`. However, traditional software engineering metaphors (Kernel, Protocol, Spec) carry loaded semantic baggage and often blur definition with execution. 

## Options Considered
1. **Status Quo (`INTAKE_BOOTSTRAP.md`):** Keep all definitions and instructions tangled in one file. Leads to brittle, bloated documentation.
2. **The Engineering Split (`ONTOLOGY.md` / `INSTRUCTIONS.md`):** A strong split, but still relies on high-level English concepts that might be misinterpreted or inconsistently named across different agentic projects.
3. **Linguistic Primitives (`WHAT-nnnn`, `WHY-nnnn`, `HOW-nnnn`):** Strip away all jargon and force all core architectural documents to be prefixed with the absolute primitives of reasoning.

## Decision
We decided to adopt the **Linguistic Primitives (`WHAT/WHY/HOW`)** structure. All core governance artifacts must be decoupled and prefixed with these terms.

## Rationale
"Primitives work best." By using absolute linguistic primitives, we achieve several massive advantages for an LLM-driven Agentic Architecture:
1. **Zero Ambiguity:** An Agent reading a `WHAT-` file instantly knows it is reading immutable state and definitions. An Agent reading a `HOW-` file instantly knows it is receiving imperative execution instructions.
2. **Psychological Enforcement of Orthogonality:** It is practically impossible for an author (Human or AI) to accidentally write step-by-step code execution logic inside a file named `WHY-0001.md`. The prefix physically enforces the separation of concerns.
3. **Perfect RAG Filtering:** If an Agent is instructed to execute a task, its retrieval system can instantly filter exclusively for `HOW-*.md` documents, ignoring the philosophical noise of `WHY-` documents, drastically improving context window efficiency.
