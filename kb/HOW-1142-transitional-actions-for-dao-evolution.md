# HOW-1142: Transitional Protocols for Dao Evolution

This document defines the strict transitional protocols and continuation actions required to maintain systems compliance and semantic coherence when the system name (SPAO → SPAOR), repository name, or glossary-driven taxonomy evolves.

---

## 1. Lexical and Semantic Evolutions
When core architectural terms evolve (e.g., transitioning from SPAO to SPAOR, or North Star to Telos):

1. **Dual-Term Coexistence**: During transition phases, both the legacy and evolved terms are permitted under explicit exceptions in `lexical_guard` rules.
2. **Automated Coherence Sweeps**: Lexical guards and validation daemons must be updated immediately to enforce the evolved term as the target, mapping legacy references to a deprecated register.
3. **Core API / Env Preservation**: Critical interface points (such as environment variables e.g. `SPAO_WORKSPACE_DIR` or CLI scripts like `bin/spao`) must remain backwards compatible or alias directly to the new terms to prevent disrupting active execution runtimes.

## 2. Repository Renaming and Relocation
When the repository identity or path changes (e.g., `agent-antigravity` → `dz-cil`):

1. **Config Harmonization**: Update all local configuration pointers (`dz-cil.yml`), system variables, and test assertion paths concurrently.
2. **Remote Refactoring**: Update GitHub remotes and upstream tracking branches. Verify that issue templates, label parsers, and metadata generators reflect the new repository name.
3. **Worktree Realignment**: Clean, prune, and re-checkout all active worktrees to align local paths with the new directory name to prevent nested workspace leakage.
