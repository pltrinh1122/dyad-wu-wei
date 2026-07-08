# Plan: Resolve Queue Desync Bug (PR #2495)

## Overview
The retro artifact `retro-2495-queue-desync.md` identified a "Temporal State-Desync Fallacy" where the Agent incorrectly assumed the state of PR #2495 without dynamically re-asserting it. Specifically, the `execute_insight` orchestration pipeline in `kernel/daemon_rt.py` is missing the dynamic state-assertion logic (`get_pr_status()`) that was previously implemented for `execute_hotfix`.

This implementation plan details how to harmonize `execute_insight` with `execute_hotfix` to strictly enforce the **Zero-Trust Memory** invariant.

## Root Cause Analysis
In `kernel/daemon_rt.py`, the `execute_insight` function currently concludes by opening a Pull Request and unconditionally emitting a success message:

```python
    pr_url = github_client.create_pull_request(title, message, branch_name)
    print(f"Insight PR created successfully: {pr_url}")
```

Because it does not check the status of the PR *after* creation, the Agent may incorrectly report that an Insight requires Operator HITL (Human-In-The-Loop) review, even if repository rules have already auto-merged it.

## Implementation Steps

### 1. Update `execute_insight` in `kernel/daemon_rt.py`
We will replace the unconditional success print statement at the end of `execute_insight` with the `get_pr_status()` verification block used in `execute_hotfix`.

> [!IMPORTANT]  
> The Agent must sleep briefly (`time.sleep(2)`) before asserting the PR status to allow remote auto-merge rules to evaluate on GitHub's side.

**Proposed Diff:**
```diff
-    pr_url = github_client.create_pull_request(title, message, branch_name)
-    print(f"Insight PR created successfully: {pr_url}")
+    pr_url = github_client.create_pull_request(title, message, branch_name)
+    print(f"Insight PR created successfully: {pr_url}")
+
+    try:
+        import time
+        time.sleep(2) # Brief sleep to allow remote auto-merge rules to evaluate
+        pr_status = github_client.get_pr_status(pr_url)
+        state = pr_status.get("state")
+        am_req = pr_status.get("autoMergeRequest")
+        
+        if state == "MERGED":
+            print(f"Insight PR {pr_url} was already MERGED by repository rules. HITL bypassed.")
+        elif am_req is not None:
+            print(f"Insight PR {pr_url} is queued for remote auto-merge. HITL bypassed.")
+        else:
+            print("Awaiting Operator review and merge (HITL). Do NOT merge autonomously.")
+    except Exception as e:
+        print("Awaiting Operator review and merge (HITL). Do NOT merge autonomously.")
```

### 2. Verify Test Suite Alignment
Before making the structural change, we must ensure any tests associated with `daemon_rt.py` or the `execute_insight` pipeline are considered. If there are unit tests mocking `github_client.create_pull_request`, we may need to also mock `github_client.get_pr_status`. 
*Note: Due to our Test-Driven Development (TDD) discipline, this step is mandatory prior to reflection.*

### 3. Execution & Reflection
Once the plan is approved, we will execute the file modification and then trigger local CI tests to guarantee structural integrity.

## Invariant Adherence
- **Zero-Trust Memory**: The system will dynamically interrogate the remote state of the PR rather than relying on assumed context.
- **Universal State-Assertion Architecture**: Both `execute_hotfix` and `execute_insight` pipelines will share identical PR state evaluation blocks, preventing pipeline-specific desynchronization.
