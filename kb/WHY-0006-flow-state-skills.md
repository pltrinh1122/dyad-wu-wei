# WHY-0006: Portable Python Skills over Raw Bash

**Date:** 2026-05-16
**Status:** Accepted

## Context
During the execution of numerous SPAO loops, the Frontier Agent frequently encountered "quote-escaping collisions" when invoking the GitHub CLI (`gh`) via raw bash to create Node Ledgers with complex markdown bodies. Furthermore, programmatically mutating files like `frontier_state.md` required brittle string-replacement operations.

## Options Considered
1. **Raw Bash (Status Quo):** Continue using `gh`, `sed`, and `git` commands natively. High cognitive overhead, high error rate due to escaping limits.
2. **CLI Wrappers (`argparse`):** Build Python scripts intended strictly for CLI invocation. Slightly better, but limits portability for future programmatic orchestrator engines.
3. **Portable Python Modules:** Abstract all Flow-State administrative actions into strictly typed, pure Python modules within the `drivers/` pillar.

## Decision
We decided to adopt **Option 3: Portable Python Modules**. 

## Rationale
Building `drivers/` as pure Python modules with deterministic functions (`create_issue`, `complete_active_node`) guarantees execution stability. It completely eliminates bash escaping errors by leveraging the standard library (`subprocess` with array arguments, native file I/O). Crucially, this design makes the skills highly portable, allowing any future LLM or generative runtime engine to seamlessly `import drivers.flow_state_manager` and autonomously orchestrate nodes without needing to learn the repository's shell intricacies.
