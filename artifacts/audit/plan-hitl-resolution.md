# Implementation Plan: HITL vs. Auto-Merge Harmonization

## Objective
To resolve the state-desync fallacy where the Agent erroneously presents a `HARD HITL BLOCK` message for a PR that has already been merged or queued for auto-merge by repository rules. We will structurally verify the PR's remote state using the GitHub API before dropping into the `Observe` phase.

## Changes Required

### 1. GitHub API Integration (`drivers/github_client.py`)
Add a new function `get_pr_status` to reliably fetch both the merge state and auto-merge queue status.

```python
def get_pr_status(pr_identifier: str) -> dict:
    """
    Returns the PR state and auto-merge request status.
    Uses: gh pr view <id> --json state,autoMergeRequest
    """
    result = _run_gh(
        ["gh", "pr", "view", str(pr_identifier), "--json", "state,autoMergeRequest"],
        capture_output=True, text=True, check=True
    )
    import json
    return json.loads(_clean_json_output(result.stdout) or "{}")
```

### 2. Standard Node Lifecyle Update (`kernel/node_lifecycle.py`)
Modify the `reflect` method around line 720. Instead of blindly assuming a PR requires a HARD HITL block when `is_autonomous_merge` is False, we will query its actual state.

```python
            else:
                try:
                    import time
                    time.sleep(2)  # Brief sleep to allow remote auto-merge rules to evaluate
                    
                    pr_status = github_client.get_pr_status(pr_url)
                    state = pr_status.get("state")
                    am_req = pr_status.get("autoMergeRequest")
                    
                    if state == "MERGED":
                        log_stage_advancement("reflect", "Reflect Phase Completed", f"PR {pr_url} was already MERGED by repository rules. HITL bypassed.")
                    elif am_req is not None:
                        log_stage_advancement("reflect", "Reflect Phase Completed", f"PR {pr_url} is queued for remote auto-merge. Bypassing HARD HITL block.")
                    else:
                        log_stage_advancement("reflect", "Reflect Phase Completed", f"PR {pr_url} successfully created. Entering Observe phase under HARD HITL block.")
                except Exception as e:
                    print(f"Warning: Failed to fetch PR status for {pr_url}: {e}")
                    log_stage_advancement("reflect", "Reflect Phase Completed", f"PR {pr_url} successfully created. Entering Observe phase under HARD HITL block.")
```

### 3. Hotfix Reflection Gate Update (`kernel/daemon_rt.py`)
Modify the `execute_hotfix` function (around line 100) where the agent statically emits the HITL block for `rt` PRs. 

```python
    try:
        import time
        time.sleep(2) # Brief sleep to allow remote auto-merge rules to evaluate
        pr_status = github_client.get_pr_status(pr_url)
        state = pr_status.get("state")
        am_req = pr_status.get("autoMergeRequest")
        
        if state == "MERGED":
            print(f"Hotfix PR {pr_url} was already MERGED by repository rules. HITL bypassed.")
        elif am_req is not None:
            print(f"Hotfix PR {pr_url} is queued for remote auto-merge. HITL bypassed.")
        else:
            print("Awaiting Operator review and merge (HITL). Do NOT merge autonomously.")
    except Exception as e:
        print("Awaiting Operator review and merge (HITL). Do NOT merge autonomously.")
```

## Outcome
When these updates are implemented:
1. The Agent's state machine will physically assert the PR's state via `gh pr view`.
2. PRs auto-merged by repository rules or pre-queued for auto-merge will no longer halt the execution loop with a false "HARD HITL" demand.
3. The Agent will seamlessly transition into the Reflect/Observe completions correctly reflecting reality.
