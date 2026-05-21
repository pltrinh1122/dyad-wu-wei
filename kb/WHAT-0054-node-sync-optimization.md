# WHAT-0054: Metasystem Integrity / Node Sync Latency Optimization — Specification

This specification defines the single-query optimization mechanism for `skills/github_client.py:list_issues_by_label` to resolve the inner-loop latency bottleneck.

## 1. Current Implementation Bottleneck
The function `list_issues_by_label` performs the following steps:
1. Executes `gh issue list --label <label> --state open --json number,title,url`.
2. Loops through the resulting list of issues, executing `gh issue view <number> --json state` for each issue to confirm its status is indeed `OPEN`.

For $N$ open issues, this pattern results in $1 + N$ shell subprocess executions and $1 + N$ network roundtrips to GitHub. Under a typical developer or multi-agent workspace with 30-40 issues, this takes upwards of 2 minutes to complete and is highly prone to network rate-limiting.

## 2. Optimized Single-Query Implementation
To achieve $O(1)$ query scaling and maximize performance, the process is consolidated as follows:

1. **Retrieve State in Initial Query**: Update the initial `gh issue list` command to request the `state` field directly in the JSON response:
   ```bash
   gh issue list --label <label> --state open --json number,title,url,state
   ```

2. **In-Memory Verification**: Parse the JSON payload and filter the issues in memory.
   An issue is considered valid if:
   ```python
   issue.get("state") == "OPEN"
   ```

3. **Subprocess Elimination**: The nested `gh issue view` loop is completely removed, reducing the subprocess and network footprint to exactly **1** query.

## 3. Reference Implementation Outline

The optimized implementation of `list_issues_by_label` inside `skills/github_client.py` will have the following signature and body:

```python
@record_execution(stage="skill")
def list_issues_by_label(label: str) -> list[dict]:
    """Returns a list of open issues matching the given label.
    
    Each item is a dict with 'number', 'title', and 'url' keys.
    Returns an empty list if no issues are found.
    """
    result = subprocess.run(
        ["gh", "issue", "list", "--label", label, "--state", "open",
         "--json", "number,title,url,state"],
        capture_output=True, text=True, check=True
    )
    import json
    issues = json.loads(result.stdout.strip() or "[]")
    
    valid_issues = []
    for issue in issues:
        # Verify the state in memory to preserve the filtering logic
        if issue.get("state") == "OPEN":
            # Strip the 'state' field if it is not expected by downstream callers,
            # or keep it as it is compatible. We keep number, title, url keys.
            valid_issues.append({
                "number": issue["number"],
                "title": issue["title"],
                "url": issue["url"]
            })
            
    return valid_issues
```

## Verification & Status
- **Status**: Pending Implementation
- **Verified by**: Node 513 Probe Plan
