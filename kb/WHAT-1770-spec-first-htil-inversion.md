# WHAT-1770: Spec-First HTIL Inversion (Anti-CI/CD Doctrine)

## 1. Intent
Invert the Hard-HITL (Human-in-the-Loop) gate. Instead of gating downstream implementation code, we gate the upstream specification (`kb/WHAT-*`). Downstream implementations (`Act` nodes) mathematically inherit the spec's alignment approval via the DAG.

## 2. Rationale (Peak Wu-wei)
We do not require complex LLM verifiers or GitHub API queries to determine if the spec was aligned. The SPAO sequence intrinsically enforces this:
- An `Act` node is strictly blocked until its prerequisite `Plan` node is merged.
- The `Plan` node requires a Hard-HITL gate because it mutates the `kb/WHAT` spec and the `contract.md`.
- Therefore, the act of actively executing an `Act` node serves as mathematically sufficient proof that the upstream spec was aligned by the Operator.
- To prevent destructive regressions, local CI tests (`spao test`) are synchronously enforced prior to reflection.

## 3. Implementation Specification
File: `kernel/node_lifecycle.py`
Target: The bypass logic inside `reflect_node()` immediately prior to the `is_admin_bypass` evaluation.

### Transformation
1. Rename the local variable `is_admin_bypass` to `is_autonomous_merge` for semantic accuracy.
2. Augment the condition to allow `is_autonomous_merge = True` if the active node phase is `act`.

```python
is_autonomous_merge = False
# 1. Existing Administrative Bypass
if not modified_files:
    is_autonomous_merge = True
elif all(f.startswith("artifacts/") and "template" not in f.lower() for f in modified_files):
    is_autonomous_merge = True

# 2. Spec-First Anti-CI/CD Bypass
elif "act" in self.phase.lower() or "act" in self.node_title.lower():
    is_autonomous_merge = True

if is_autonomous_merge:
    github_client.admin_merge_pull_request(pr_url)
```

## 4. Testing & Validation
- The local CI suite remains the ultimate deterministic gate (`test_node_lifecycle.py`).
- No changes to `daemon_status.py` or `gh` workflow.
