# Retrospective: Node 959 Reflect Failure (JSON Decode Error)

## Failure Detail
*   **Command**: `SPAO_PERSONA_ID=frontier ./bin/node reflect 959 ...`
*   **Error**: `json.decoder.JSONDecodeError: Expecting value: line 1 column 2 (char 1)`
*   **Context**: The `--invariants` argument passed to `reflect` used single quotes (`'`) for string elements inside the JSON array instead of double quotes (`"`). Python's `json.loads` strictly requires double quotes. The exception was caught by the top-level handler before the `FlowTransaction` started.

## Codified Insight
When passing JSON arrays as arguments in bash (such as for `invariants`), elements within the array must strictly use double quotes `"` in accordance with JSON specifications, wrapped in a single-quoted bash string: `'["element 1", "element 2"]'`.

## Mitigation Action
1. Created this retrospective document.
2. Re-executing the `reflect` command with correctly formatted JSON arguments.
