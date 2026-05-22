# Retrospective: Node 739

## 1. Context & Motivation
Following the Dao Portability restructure (Node 738) where `orchestrator/` became `kernel/` and `skills/` became `drivers/`, a post-sync Metasystem Integrity Audit identified a regression: raw string literals for the old directory names were left behind. This caused failures when invoking `audit_daemon.py` via `path_resolver.resolve_core_path("skills", "audit_daemon.py")`. Node 739 was initiated to clean up these lingering string literals.

## 2. Actions Taken
- **Source Code Search**: Grepped the `kernel/`, `drivers/`, `bin/`, `tests/`, and `kb/` directories for hardcoded `"skills"` and `"orchestrator"` string literals.
- **Code Modifications**:
  - Replaced `"skills"` with `"drivers"` in `kernel/mgr_node.py` and `kernel/mgr_retro.py`.
  - Replaced `"orchestrator"` with `"kernel"` in `kb/WHY-0019-ontological-refinement-telemetry.md`.
  - Fixed test assertions matching these literals in `tests/test_file_locker.py` and `tests/test_mgr_retro.py`.
- **Validation**: Executed `spao test` (`./bin/run-tests`). 214 tests passed, confirming architectural stability.

## 3. Learnings & Future Invariants
- **Refactoring Guardrails**: Pure syntactical import replacement tools (e.g., matching `import X` and `from X`) are insufficient for comprehensive architectural migrations. Hardcoded string literal paths used by dynamic path resolvers must be deliberately audited during such operations.
- **Audit Value**: This node highlighted the exact value of the Post-Sync Metasystem Integrity Audit, which caught a subtle pathing error before it could degrade future nodes.
