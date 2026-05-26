# WHAT-0034: Three-Loop Governance Framework Specification

This specification codifies the operational mechanics, tracking, and guardrails for the Three-Loop Project Governance Framework within the `dz-cil` system.

---

## 1. Backlog & State Metadata Tracking (A1, E1)

Nodes will track three orthogonal classification axes: `loop`, `area`, and `kind`.

### 1.1 GitHub Issue Labels
The following metadata label namespaces are supported:
- **Loop**: `loop:spao` (Meta-governance/policy), `loop:sdlc` (Software development/implementation).
- **Area**: `area:metasystem` (Harness self-management), `area:harness-platform` (CLI tooling and wrappers), etc.
- **Kind**: `kind:infra` (Tooling/platform), `kind:domain` (Product features).

### 1.2 Local State Representation
The `artifacts/frontier_state.yml` schema is updated. Each entry under `nodes` will contain optional attributes `loop`, `area`, and `kind` (defaulting to `null` if unspecified or not labeled):
```yaml
nodes:
  - name: 'Node 386: Probe 386: Plan - Spike Path: Three-Loop Governance Framework'
    status: '[///] Act Phase'
    learnings: Planning Phase
    invariants: []
    loop: spao
    area: metasystem
    kind: infra
```

### 1.3 State Rendering
The generated `artifacts/frontier_state.md` markdown derived log will print these properties beneath the Status line if they are present:
```markdown
## Node 386: Probe 386: Plan - Spike Path: Three-Loop Governance Framework
- **Status**: [///] Act Phase
- **Loop**: spao
- **Area**: metasystem
- **Kind**: infra
- **Learnings & Context**: Planning Phase
```

---

## 2. Partitioned Worktree Directory Layout (C1 - Option B)

To physically segregate workspace contexts on disk, active checkouts will be routed according to their loop classification.

### 2.1 Workspace Routing Rules
When executing `spao node checkout <issue_id> <branch_name>`:
- If the node's issue has label `loop:spao`, establish the worktree path at:
  `.worktrees/spao/<branch_name>/`
- If the node's issue has label `loop:sdlc`, establish the worktree path at:
  `.worktrees/sdlc/<branch_name>/`
- Fallback/default path (for unlabeled or other loops):
  `.worktrees/node/<branch-name>/`

### 2.2 Cleanup Integration
All clean/cleanup scripts (including `spao node sync` and `spao node reflect` post-merge hooks) must scan and clean up these partitioned paths dynamically.

---

## 3. Configurable PR Purity Verification (C2)

### 3.1 Purity Validation Rule
For any active branch classified as `loop:spao`, the branch MUST NOT introduce modifications to executable code paths.
- **Policy Paths Only**: SPAO commits are restricted to modifying `kb/**` and `artifacts/**` directories, as well as `GEMINI.md`.
- **Enforcement Action**: If a violation is found, `spao node reflect` will raise a validation exception and block push/PR creation.

### 3.2 Configuration Parameter
This check is toggled via `dz-cil.yml` at the root of the repository:
```yaml
governance:
  spao_purity_enforcement: true
```
If set to `false`, a warnings is printed but reflection is permitted to proceed.

---

## 4. SPEC Gate checklists & Enforcement (B1, B2)

### 4.1 Planning Checklists
Every generated `task.md` template and active implementation plan must contain the following checkbox entries:
- `[ ] SPEC Gate-1: Operator approved design`
- `[ ] SPEC Gate-2: Agent/Builder verified implementable with no ambiguity`

### 4.2 Spec File Tracking Enforcement
When `spao node plan-finish` is executed:
- The system must verify that a corresponding `WHAT-` specification file (e.g. `kb/WHAT-*.md` or matching name) has been created and staged/tracked in git index.
- If no spec file is present, `plan-finish` will fail with an explicit validation error, blocking transition to the Act phase.

---

## 5. Loop Transition Summaries in PRs (D1)

When generating PR descriptions in `spao node reflect`, the agent must append the following template:

```markdown
## Three-Loop Transition Summary
- **Source Loop**: [SPAO / SDLC]
- **Target Lineage**: main
- **Gate Status**: Gate-1 [OK], Gate-2 [OK]

### Observed Variances & Recommendations
[List any design or execution variances observed during the run, along with recommendations for SDLC loop improvement]
```
