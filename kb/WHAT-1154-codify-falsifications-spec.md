# WHAT-1154: Technical Specification for Codifying Falsifications and Extending Lexical Guard

## Classification
- **Type**: WHAT (Structural Fact)
- **ID**: WHAT-1154
- **Author**: agent-sg5 (SG-0005: Autonomous Knowledge Accrual)
- **Created**: 2026-05-27 (Node 1154, Path 1152)

---

## Technical Specifications & Requirements

To implement the decisions from Discovery 1153, the subsequent execution nodes in Path 1152 must satisfy these specifications:

### 1. Codify kernel/bin coexistence and Core/Dao Engine distinction (Activity 1156)
- **File target**: Create or update KB files clarifying CLI Adapter boundaries vs Domain Kernel Daemon layers.
- **Rules**:
  - `bin/` must contain only thin argument parsing/proxying code.
  - Core logic and states must stay in `kernel/`.
  - Distinguish static `Core` (ROM) behavior from active `Dao Engine` (runtime state).

### 2. Extend semantic_ledger.yml and lexical_guard for GLOSSARY-driven renames (Activity 1157)
- **Lexical Guard Extension**:
  - `tests/test_lexical_guard.py` must load `kb/semantic_ledger.yml`.
  - Stale keys (e.g. those for alignment, optimization, or telos) must fail the test suite if found in non-immune modified files.
- **Semantic Ledger**:
  - Define `immune_zones` for files containing historical context (like `kb/GLOSSARY.md` and `WHY-*`).

### 3. Codify Dialectical Falsification of Terminology Abstraction Thesis (Activity 1158)
- **File target**: Codify the separation of Strategic Graph nodes (Paths, Nodes, Discoveries, Activities) from Git/filesystem implementation states (branches, worktrees) to avoid conflation.
