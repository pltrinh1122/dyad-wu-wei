# WHAT-0636: Multi-Tenant Concurrent Agent State Specification

## Classification
- **Type**: WHAT (Specification)
- **ID**: WHAT-0636
- **Author**: agent-ziran
- **Created**: 2026-05-29 (Node 636, Path 634)
- **Status**: Draft

---

## 1. Goal

Establish a multi-tenant tracking schema in the repository's topological ledger to allow multiple agent personas to execute parallel loops concurrently. This prevents state-pointer conflicts and overwrites.

---

## 2. Technical Specification

### 2.1 Ledger Schema Migration (`frontier_state.yml`)

The singleton root-level active pointers in the topological YAML ledger must be migrated to a nested structure under an `active_agents` key, mapped by the active agent's Persona ID.

#### 2.1.1 Legacy Format
```yaml
current_active_path: "Path 634: Path: Refactor frontier_state for concurrent agent awareness"
current_active_node: "Node 636: Node 636: Discovery 636: Plan - Path: Refactor frontier_state for concurrent agent awareness"
```

#### 2.1.2 Multi-Tenant Format
```yaml
active_agents:
  agent-ziran:
    current_active_path: "Path 634: Path: Refactor frontier_state for concurrent agent awareness"
    current_active_node: "Node 636: Node 636: Discovery 636: Plan - Path: Refactor frontier_state for concurrent agent awareness"
  agent-platform:
    current_active_path: null
    current_active_node: null
```

### 2.2 Human-Readable Documentation Migration (`frontier_state.md`)

The human-readable tracking ledger must also reflect the multi-tenant active agents state under a unified section, replacing the legacy singleton headers.

#### 2.2.1 Legacy Section
```markdown
## Current Active Path
**Path 634: Path: Refactor frontier_state for concurrent agent awareness**

## Current Active Node
**Node 636: Node 636: Discovery 636: Plan - Path: Refactor frontier_state for concurrent agent awareness**
```

#### 2.2.2 Multi-Tenant Section
```markdown
## Active Agents Matrix
* **agent-ziran**:
  - Current Active Path: `Path 634: Path: Refactor frontier_state for concurrent agent awareness`
  - Current Active Node: `Node 636: Node 636: Discovery 636: Plan - Path: Refactor frontier_state for concurrent agent awareness`
* **agent-platform**:
  - Current Active Path: `None`
  - Current Active Node: `None`
```

### 2.3 Implementation Requirements

#### 2.3.1 Environment Resolution
- The system resolves the current persona by reading the `SPAO_PERSONA_ID` environment variable.
- If the environment variable is not defined or is empty, the system defaults to `agent-default`.

#### 2.3.2 Reader/Writer Logic
- **Read Operations**: The state parser reads from `active_agents[SPAO_PERSONA_ID]` to determine the active path and node coordinates.
- **Write Operations**: The state updater writes exclusively to the nested structure under `active_agents[SPAO_PERSONA_ID]`, preserving entries for other personas.
- **Backward Compatibility**: If the `active_agents` key is absent, the system falls back to reading the legacy root-level singleton pointers.

#### 2.3.3 CLI Tooling Integration
- CLI wrappers and diagnostics queries must resolve active paths and nodes by looking up the tenant matching the current environment context.
