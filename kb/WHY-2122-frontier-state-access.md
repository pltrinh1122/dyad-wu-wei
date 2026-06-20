# Epistemic Insight: Frontier State Access Pattern

**Issue ID**: 2122
**Source**: `artifacts/audit/retro-2112.md`

## Context
During execution of Node 2112, a system crash occurred due to attempting to call `kernel.agent_frontier.read_active_nodes`, a function that does not exist in the codebase.

## The Rule
When interacting with `artifacts/frontier_state.yml` to read active agents or locks:
- **DO NOT** attempt to guess or hallucinate helper functions like `read_active_nodes`.
- **DO** use the foundational `agent_frontier.load_state(frontier_file)` method to load the dictionary.
- Extract the `"active_agents"` mapping directly from the returned state dictionary.

**Example:**
```python
from kernel import agent_frontier

state = agent_frontier.load_state("artifacts/frontier_state.yml")
active_agents = state.get("active_agents", {})
```

## Lexical Precision
Be extremely careful not to use legacy terms or hallucinated variable names for the `kernel_daemon`. The orchestrator persona is strictly the `kernel_daemon`, and the primary access pattern for the frontier state is `load_state()`.
