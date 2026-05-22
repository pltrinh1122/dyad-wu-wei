# Retro 738

## Failure Context
During the physical restructuring of the DZ-OS (renaming `orchestrator/` to `kernel/` and `skills/` to `drivers/`), the initial local test harness (`./bin/run-tests`) threw two failures:
1. `test_get_core_dir` failed because it explicitly asserted the existence of `skills/`.
2. `test_modified_files_lexical_compliance` failed because the `replace_imports.py` script inadvertently touched `kb/WHY-0013-normalized-status-labels.md`, exposing the deprecated word "epic" to the Lexical Guard checker.

## Lesson Learned
When performing global string replacements across a repository, any modified files will automatically trigger the `test_lexical_guard.py` checks on those files. If legacy documents contain deprecated terms, touching them will force an immediate compliance update. Additionally, structural tests that assert hardcoded directory names must always be audited as part of a directory rename operation.

## Knowledge Accrual
- No immutable invariants were violated.
- I successfully remediated the issues by updating `test_path_resolver.py` to assert the existence of `drivers/` instead of `skills/`, and I manually remediated the word "epic" to "path" in `WHY-0013`. The test suite subsequently passed 100%.
