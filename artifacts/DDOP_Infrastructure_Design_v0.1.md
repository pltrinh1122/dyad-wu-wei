# Domain Dao Onboarding Protocol (DDOP) Infrastructure Design v0.1

## 1. Gap Analysis: Toolchain Incompatibilities (Wu-wei vs Familyloom)

### 1.1 Branching & Worktree Orchestration
- **Familyloom (`tools/repo` & `tools/scm`):** Requires strict adherence to `solo/<anchor>/<alias>/<slug>` naming conventions and enforces GC lifecycle checks (`INV-OH-008`). It also uses Prefect states for multi-branch Forward-Port Waves.
- **Wu-wei Engine (`SPAO / bin/node`):** Uses `.worktrees/node/<id>-<slug>` taxonomy and manages its own `frontier_state.yml` locking mechanism.
- **Gap:** Antigravity executing a node inside Familyloom will violate `INV-OH-001` (Worktree Strictness) unless the SPAO checkout command dynamically adopts the target domain's branch nomenclature.

### 1.2 Integration Validation
- **Familyloom:** Demands `tools/repo content-parity` checks for deployed source-of-truth files and `forward_port_linter.py` for governance sync.
- **Wu-wei Engine:** Executes generic `./bin/run-tests` or `spao test` before `reflect`.
- **Gap:** The local CI verification discipline in Wu-wei must be extended to dynamically load and invoke domain-specific verification scripts prior to PR creation.

### 1.3 Auto-Merge Governance
- **Familyloom:** Mandates `gh pr merge --squash --auto` for Forward-Port PRs when CI passes, bypassing operator review (per `H7 Forward-Port PR auto-approval protocol`).
- **Wu-wei Engine:** Defines its HTIL bypass through `dyad-wu-wei.yml` `sacred_files`.
- **Gap:** Wu-wei's `node_lifecycle.py` HTIL block must natively recognize Familyloom's Class 3 Exempt Operations and Forward-Port auto-approvals, yielding merge authority to the domain's doctrine rather than halting for HITL.

### 1.4 Test-First Discipline
- **Familyloom:** Enforces strict RED -> GREEN widget/integration testing via Flutter.
- **Wu-wei Engine:** Optimized for Python/CLI test generation.
- **Gap:** Agents operating on Familyloom need explicit prompt injection for `flutter test` execution and Mocktail usage (per `FL-TOOL-001`) to maintain compliance.

## 2. DDOP Infrastructure Design

### 2.1 Support Line (SLA)
- **Definition:** The Support Line governs the cross-repository compatibility contract. When Familyloom's governance updates (e.g., a new `FL-INV`), the Wu-wei engine MUST synthesize and adapt to it within a single SPAO node cycle.
- **Enforcement:** A daemon `audit_domain_sync.py` will monitor the SHA hashes of Familyloom's Tier 1 governance docs. Drift will trigger an automated Node creation in Wu-wei to parse the new rules and adjust SPAO plugins.

### 2.2 Domain Registry (`dyad-wu-wei.yml`)
The Wu-wei configuration must be extended to maintain a registry of external managed domains:
```yaml
domains:
  family_legacy:
    path: /mnt/shared_data/git_repos/family_legacy/main
    domain_dao_digest: artifacts/Domain_Dao_Digest_v0.1.md
    branch_prefix: solo/main
    validation_hook: tools/lint/run_all.sh
```

### 2.3 Onboarding Checklist for New Domains
To onboard a new external project under the Domain Dao protocol, the Operator/Agent MUST complete:
- [ ] 1. **Ingest & Synthesize:** Survey the external repository's governance corpus and extract its invariants into a Domain Dao Digest artifact.
- [ ] 2. **Map Toolchain Overlaps:** Identify conflicts between the project's native scripts (e.g., `tools/repo`) and Wu-wei's SPAO executors.
- [ ] 3. **Register Domain:** Add the domain's path, hooks, and prefixes to `dyad-wu-wei.yml` under the `domains` key.
- [ ] 4. **Test CI Hook:** Execute a dry-run Node targeting the domain to verify that `node_lifecycle.py` correctly delegates local CI verification to the domain's native linters.
- [ ] 5. **Ratify Integration:** Operator reviews the DDOP Gap Analysis and merges the configuration update.
