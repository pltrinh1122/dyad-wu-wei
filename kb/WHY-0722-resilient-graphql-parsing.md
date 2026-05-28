# WHY-0722: Resilient GraphQL Parsing in GitHub Client

## 1. The Phenomenon
The GitHub CLI (`gh`) periodically outputs GraphQL API deprecation warnings or operational diagnostic alerts to `stderr` or, depending on shell configuration and versioning, prepends them to the captured output streams. 
When these warnings occur, standard calls like `gh issue view` or `gh pr list` returning JSON payloads fail to parse cleanly under strict JSON parsers (`json.loads`), causing the Next-Best-Action (NBA) evaluator or flow lifecycle orchestrators to crash or fail-closed.

## 2. Root Cause Analysis
Antigravity CLI wrapper commands execute the `gh` tool via `subprocess.run` (proxied by `_run_gh` inside `drivers/github_client.py`). Many of these commands capture stdout using `capture_output=True` and attempt to decode the raw output directly:
```python
json.loads(result.stdout.strip() or "[]")
```
If the environment or the `gh` executable introduces warning text or non-JSON telemetry lines (e.g. `warning: ...` or deprecation alerts), the raw string returned from `stdout` is no longer a syntactically valid JSON document, resulting in a `json.decoder.JSONDecodeError`.

## 3. The Mitigation Strategy
To prevent raw stdout contamination from breaking the JSON parser:
1. We must filter out any non-JSON prefix/suffix lines from the stdout stream before passing it to `json.loads`.
2. A robust JSON regex scanner or line-by-line parser can identify the starting position of the JSON boundary (e.g., matching the first `{` or `[` character).
3. Alternatively, we can define a clean string helper `_clean_json_output` that strips off leading or trailing non-JSON warning lines.

*This mitigation plan is formally mapped to Probe 723 and Activity 724.*
