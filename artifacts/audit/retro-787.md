# Retrospective: Node 787

## Execution Failure
During the execution of Node 787, the following failures occurred:
1. `test_modified_files_lexical_compliance` failed because the rename script touched files that contained legacy strings ("epic" and "spike"), causing them to be flagged by the lexical guard since they were now considered "modified files".
2. `test_execute_next_best_action_hook` failed due to `StateCorruptionError: Frontier state checksum mismatch!` because the `artifacts/frontier_state.yml` was directly modified by the string-replacement script without updating its corresponding `.sha256` checksum file.
3. `test_load_nodes_and_paths` failed because modifying the regex in `daemon_retro.py` to remove `Activity` and add `Node` unintentionally broke the parsing of historical nodes containing the legacy `Spike Path` string in their names.

## Root Cause
- The string-replacement regex modified files with legacy terms, triggering the lexical guard.
- Direct file modification bypassed the `flow_state_manager` checksum sync.
- Changing `type_regex` in `daemon_retro.py` without understanding the test data's reliance on legacy names.

## Mitigation
- Replaced "epic" with "path" and "spike" with "probe" in the modified files.
- Ran `./bin/meta rehash` to repair the frontier state checksum.
- Restored `daemon_retro.py` regex fallback logic to properly ignore the `Node` match so the fallback can handle historical `Spike Path` strings correctly while satisfying the requirement to remove `Activity`.

## Codified Insight
When running broad string replacements on legacy files, you must be aware of lexical guards that will trigger if previously exempt files are modified. Additionally, changes to `artifacts/frontier_state.yml` MUST be immediately followed by `./bin/meta rehash`.
