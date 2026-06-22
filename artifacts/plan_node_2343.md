# Technical Design Plan: Semantic Dispatcher for Cross-Path Dependency Tracking

## Overview
The objective is to prevent concurrent execution of structurally dependent nodes across different paths that belong to the same Strategic Goal (SG) domain. This prevents costly merge conflicts that occur when dependent paths are executed in parallel by different sub-agents.

We will build a "Semantic Dispatcher" into the Next-Best-Action (NBA) Scorer. It will query the active SG domains currently being worked on by *other* active sub-agents. If a candidate node belongs to an SG domain that is already actively executing elsewhere, its dependency score (`c_dep`) will be zeroed out, effectively deferring its dispatch.

## Proposed Changes

### 1. `kernel/nba_scorer.py`
We will inject a new semantic dependency check within the `calculate_score` method of the `NBAScorer` class.

**Implementation Details:**
```python
--- a/kernel/nba_scorer.py
+++ b/kernel/nba_scorer.py
@@ -118,6 +118,36 @@ class NBAScorer:
                     except Exception:
                         c_dep = 0.0
                         break
+                        
+        # Semantic Dispatcher: Cross-Path Dependency Tracking
+        if c_dep > 0.0:
+            try:
+                from kernel import agent_frontier
+                yml_path = agent_frontier.resolve_yml_path(self.frontier_file)
+                state = agent_frontier.load_state(yml_path)
+                active_agents = state.get("active_agents", {})
+                my_persona = _get_active_persona()
+                
+                ledger = daemon_strategic.load_ledger()
+                other_active_sgs = set()
+                
+                # Find SG domains being executed by OTHER agents
+                for persona, data in active_agents.items():
+                    if persona == my_persona:
+                        continue
+                    
+                    for key in ["current_active_node", "current_active_path"]:
+                        val = data.get(key)
+                        if val:
+                            import re
+                            match = re.search(r"#(\d+)", val)
+                            if match:
+                                active_id = match.group(1)
+                                sg_domain = _get_sg_domain_for_issue(active_id, ledger)
+                                if sg_domain:
+                                    other_active_sgs.add(sg_domain)
+                                    
+                # Determine Candidate's SG Domain
+                candidate_sg = _get_sg_domain_for_issue(node_id_str, ledger)
+                if candidate_sg and candidate_sg in other_active_sgs:
+                    c_dep = 0.0  # Defer dispatch
+            except Exception:
+                pass
```

### 2. Helper Function `_get_sg_domain_for_issue`
We will define a private helper within `kernel/nba_scorer.py` to efficiently look up the SG domain for any given issue ID:

```python
def _get_sg_domain_for_issue(issue_id: str, ledger: dict) -> str | None:
    # 1. Check if the issue itself is a prioritized path in any SG
    for goal in ledger.get("strategic_goals", []):
        if str(issue_id) in [str(p) for p in goal.get("prioritized_paths", [])]:
            return goal.get("id")
            
    # 2. If it's a node, find its parent path and check again
    try:
        path_id = daemon_strategic.find_parent_path_id(issue_id)
        if path_id:
            for goal in ledger.get("strategic_goals", []):
                if str(path_id) in [str(p) for p in goal.get("prioritized_paths", [])]:
                    return goal.get("id")
    except Exception:
        pass
        
    return None
```

## How It Works
1. When `NBAScorer.calculate_score()` evaluates a candidate node, it looks at `frontier_state.yml` to see what paths/nodes are currently locked by *other* active sub-agents.
2. It maps these active issue IDs to their respective Strategic Goal (SG) domains using the strategic ledger.
3. It identifies the candidate node's parent Path and looks up its corresponding SG domain.
4. If the candidate node's SG domain intersects with any of the `other_active_sgs`, `c_dep` is immediately set to `0.0`. This gracefully drops the node's score to 0, deferring it until the SG domain becomes free.
