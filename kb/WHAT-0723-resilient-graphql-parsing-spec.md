# WHAT-0723: Resilient GraphQL Parsing Specification

## 1. Context
The GitHub Client (`drivers/github_client.py`) uses the GitHub CLI (`gh`) to query repository information. Some environments or newer versions of `gh` print GraphQL deprecation warnings or diagnostics to `stdout` alongside the JSON payload. This contaminates the output, causing `json.loads()` to raise a `JSONDecodeError`.

## 2. Technical Invariants

### 2.1 JSON Output Cleaning Helper
We must introduce a helper function `_clean_json_output` inside `drivers/github_client.py`:
```python
def _clean_json_output(stdout: str) -> str:
    """Strips GraphQL deprecation warnings and other non-JSON text from stdout."""
    cleaned = stdout.strip()
    if not cleaned:
        return cleaned
    # Find the start of the JSON block (either '{' or '[')
    start_curly = cleaned.find('{')
    start_bracket = cleaned.find('[')
    
    if start_curly == -1 and start_bracket == -1:
        return cleaned  # Fallback to original stripped output
        
    if start_curly != -1 and start_bracket != -1:
        start_idx = min(start_curly, start_bracket)
    else:
        start_idx = start_curly if start_curly != -1 else start_bracket
        
    return cleaned[start_idx:]
```

### 2.2 Integration Points
All functions inside `drivers/github_client.py` that parse `stdout` via `json.loads` must process the output through `_clean_json_output` before parsing. This includes:
1. `list_issues_by_label`
2. `get_open_issues`
3. `get_issue_details`
4. `get_issue_comments`
5. `create_pull_request`
6. `get_open_prs`
7. `get_merged_prs`
8. `get_issue_labels`

## 3. Verification Plan
We will write a comprehensive unit test suite in `tests/test_github_client_resilience.py` to verify that `_clean_json_output` correctly handles contaminated stdout containing multiple lines of deprecation warning followed by the valid JSON payload.
