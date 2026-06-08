# DDOP Technical Specification

## 1. Objective
Design the codebase changes required to support the Domain Dao Onboarding Protocol (DDOP) across the Wu-wei engine, allowing the engine to seamlessly transition operations to external domains (e.g., `family_legacy`) while respecting their specific governance (linters, branch rules, HTIL limits).

## 2. Configuration Schema Extension (`dyad-wu-wei.yml`)
The core configuration must introduce a `domains` registry to map external projects and define domain-specific hooks.

### Proposed Schema Addition:
```yaml
domains:
  [domain_id]:
    path: [absolute_path_to_repository_root]
    domain_dao_digest: [path_to_digest_artifact]
    branch_prefix: [string_prefix_for_branches, e.g., 'solo/main/']
    validation_hook: [script_path_for_local_ci]
    auto_approve_labels: [list_of_labels_that_trigger_htil_bypass]
```
**Changes:** 
- Introduce `kernel/config_parser.py` or modify existing parsers to read the `domains` block and expose `get_domain_config(domain_id)`.

## 3. Worktree Orchestration (`kernel/node_lifecycle.py`)
When a node is assigned to an external domain (inferred via label `domain:family_legacy` or node metadata), the check-out and reflection operations must adapt.

### 3.1 Domain-Aware Checkout
- Currently, `node checkout` creates a worktree in `.worktrees/node/<id>-<slug>`.
- **Change:** For domain nodes, branch names must prepend `branch_prefix`. E.g., `solo/main/<id>-<slug>` instead of `node/<id>-<slug>`. Worktree isolation remains local to Wu-wei or uses the target domain's worktree structure.

### 3.2 Domain-Aware CI Validation
- Currently, `node reflect` executes `./bin/run-tests` unconditionally.
- **Change:** `node_lifecycle.py` (lines 497-503) will query `get_domain_config()`. If `validation_hook` is present, it will execute that hook instead of `./bin/run-tests`.

### 3.3 Domain-Aware HTIL Bypass
- Currently, `node_lifecycle.py` bypasses HTIL only for `sacred_files` (e.g., `GEMINI.md`).
- **Change:** Extend HTIL bypass logic (lines 600+) to recognize external domain auto-merge conditions (e.g., Forward-Port tags). If an issue has a domain-exempt label, `gh pr merge --squash --auto` is authorized.

## 4. Context & Prompts (`kernel/daemon_knowledge_accrual_extra.py`)
- **Change:** Modify agent bootstrap/prompt compilation to inject `domain_dao_digest` into the system prompt when operating on a domain node, ensuring the agent adheres to FL-ARCH and FL-INV constraints.

## 5. Next Steps
- Execute the changes outlined above across the `kernel` module.
- Update testing harnesses to mock domain registries.
