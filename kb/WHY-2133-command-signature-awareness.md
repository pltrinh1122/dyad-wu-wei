# Epistemic Insight: Command Signature Awareness

**Issue ID**: 2133
**Source**: `artifacts/audit/retro-2101.md`

## Context
During execution of Node 2101, an attempt was made to run `bin/node reflect 2100` without providing the required positional arguments. This blind execution assumption led to a system crash and the generation of an execution failure telemetry event.

## The Rule
When executing custom CLI tools (e.g., `bin/node`), **do not assume** argument signatures or expect interactive prompts unless explicitly verified.
- **DO** verify the exact argument signature of custom bin tools before invoking them.
- For example, `bin/node reflect` strictly requires multiple positional arguments: `issue_id`, `node_name`, `learnings`, `invariants`, `commit_msg`, and `branch_name`.

**Example of Correct Usage:**
```bash
bin/node reflect 2133 "Path 2098: Reflect" "Learnings" "- invariant 1" "commit message" "branch/name"
```

## Impact
Blind execution without argument verification causes avoidable crashes, disrupting the Continuous Inference Loop and generating unnecessary failure telemetry.
