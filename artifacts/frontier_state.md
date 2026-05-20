# Agentic Frontier State

## Node 0: Agentic Initialization & Flow-State Setup
- **Status**: Completed
- **Learnings & Context**: Injected `AGENT.md` and established the topological `frontier_state.md` to persist the session architecture.
- **Feedforward Invariants**:
  - `[x]` `AGENT.md` is present.
  - `[x]` Flow-state anchor is established.

## Node 1: Formulate INTAKE_BOOTSTRAP.md Specification
- **Status**: Completed
- **Learnings & Context**: Drafted the core `INTAKE_BOOTSTRAP.md` standard based on the `agent-travel` case study, defining the GH-Issue flow-state anchor and Agent vs Operator responsibility matrix.
- **Feedforward Invariants**:
  - `[x]` `INTAKE_BOOTSTRAP.md` successfully captures the standards.

## Node 2: Dry-Run Agentic Architecture Compliance
- **Status**: Completed (Dry-Run)
- **Learnings & Context**: Executed the `INTAKE_BOOTSTRAP.md` SPAO loop on the meta-repository itself. Created GH Issue #3 as the Flow-State Ledger. Validated that `skills/` and `orchestrator/` directories can be scaffolded following the standard.
- **Feedforward Invariants**:
  - `[x]` Full Agentic Architecture (`artifacts/`, `skills/`, `orchestrator/`) is present.
  - `[x]` GH Issue successfully acted as the Plan anchor.

## Node 3: Codify Side-Bar Rubrics & Materialization Boundary
- **Status**: Completed
- **Learnings & Context**: Materialized the off-ledger evaluation regarding conversational interaction vs GH-Issue strictness. `INTAKE_BOOTSTRAP.md` was updated to explicitly define the Side-Bar Rubrics and the Materialization Boundary, ensuring future agents consistently interpret when to chat freely versus when to demand a GH-Issue.
- **Feedforward Invariants**:
  - `[x]` Agent consistency rubrics are codified in the standard.

## Node 4: Codify Hybrid Epic-Ledger Issue Governance
- **Status**: Completed
- **Learnings & Context**: Materialized the hybrid approach to GitHub Issue lifecycle management. Established the pattern of a long-lived "Epic Meta-Index" for macro-tracking and ephemeral "Node Issues" for immutable micro-transactions. This bridges the gap between clean audit narratives and strict execution contracts.
- **Feedforward Invariants**:
  - `[x]` The SPAO loop standard mandates updating the Epic Meta-Index during Plan and Reflect phases.

## Node 5: Implement Key Decision Record (KDR) Knowledge Base
- **Status**: Completed
- **Learnings & Context**: Materialized the `artifacts/kdr/` Knowledge Base structure. Identified that while GH-Issues capture the *execution*, KDRs are required to capture the *philosophical rationale* of Side-Bar conversations. Generated foundational KDRs (0001 and 0002) to establish the repository's philosophical memory.
- **Feedforward Invariants**:
  - `[x]` The SPAO standard mandates a KDR Handoff before GH-Issue creation for major architectural decisions.

## Node 6: Establish Formal Bootstrap Audit Control Artifact
- **Status**: Completed
- **Learnings & Context**: Successfully executed the "KDR Handoff" pattern. Generated KDR-0003 to document the decision to use dynamic GH-Issue ledgers for auditing. Created the master `BOOTSTRAP_AUDIT_TEMPLATE.md` control artifact and updated `INTAKE_BOOTSTRAP.md` to mandate the audit phase before a repository begins operations.
- **Feedforward Invariants**:
  - `[x]` Formal Audit template exists and is integrated into the intake bootstrap process.

## Node 7: Migrate to Primitive WHAT/WHY/HOW Architecture
- **Status**: Completed
- **Learnings & Context**: Successfully crossed the Materialization Boundary to completely restructure the repository's governance documents. De-jargonized the standards into pure linguistic primitives: `WHAT-*` for Definitions/Ontology, `WHY-*` for Decision Rationale, and `HOW-*` for Instructions. This creates an unambiguously orthogonal system for LLM interpretation.
- **Feedforward Invariants**:
  - `[x]` All core files enforce the `WHAT/WHY/HOW` primitive prefix.

## Node 8: Establish the Knowledge Base (kb/) Pillar
- **Status**: Completed
- **Learnings & Context**: Materialized the 4-pillar architecture by isolating all linguistic primitives into the `kb/` directory. This creates perfect architectural symmetry: `artifacts/` (RAM), `skills/` (Hands), `orchestrator/` (Engine), and `kb/` (ROM).
- **Feedforward Invariants**:
  - `[x]` The repository root is clean, and the `kb/` directory is the authoritative source for system laws.

## Node 9: Formal Bootstrap Self-Audit
- **Status**: Completed
- **Learnings & Context**: Created the Epic Meta-Index issue to satisfy governance invariants. Generated the formal Bootstrap Audit Issue. Programmatically verified the existence of `AGENT.md`, `frontier_state.md`, the 4 pillars (`artifacts/`, `skills/`, `orchestrator/`, `kb/`), and the GH-Issue tracking model.
- **Feedforward Invariants**:
  - `[x]` The repository has passed the Bootstrap Audit and is officially cleared for "Operations."

## Node 10: Codify Audit Remediation Threshold
- **Status**: Completed
- **Learnings & Context**: Established the "Complexity Threshold" rule for audits. Agents are now permitted to execute atomic "Audit + Remediate" operations for trivial, deterministic fixes (to maintain velocity), but are strictly required to spawn dedicated GH-Issue Nodes for complex logic fixes (to prevent masked mutations).
- **Feedforward Invariants**:
  - `[x]` Audits allow trivial inline remediation; complex failures demand dedicated spin-out nodes.

## Node 11: Formal Bootstrap Self-Audit V2
- **Status**: [///] Observe Phase (Paused for HITL)
- **Learnings & Context**: Re-executed the audit to ensure compliance with the newly codified `kb/WHY-0004` Threshold Rule.
- **Feedforward Invariants**:
  - `[ ]` Await final operator sign-off before closing the ledger.

## Node 12: Materialize Audit Payload Artifacts
- **Status**: Completed
- **Learnings & Context**: Materialized the "Ledger vs Payload" paradigm for audits. The GH-Issue serves as the micro-state execution contract, but the final diagnostic result is permanently outputted to `artifacts/audit/`. This provides excellent offline, chronological traceability of repository health. Generated the first payload: `0001-bootstrap-v2-compliance.md`.
- **Feedforward Invariants**:
  - `[x]` All future audits must generate a physical payload in `artifacts/audit/` prior to ledger closure.

## Node 13: Implement Portable Flow-State Skills
- **Status**: Completed
- **Learnings & Context**: Successfully replaced brittle bash commands with pure Python modules via rigorous TDD. Flow-State operations (Plan/Reflect) are now safely executed via skills.flow_state_manager.
- **Feedforward Invariants**:
  - `[x] TDD test suite achieves 100% pass rate`

## Node 14: Implement Testing Harness Skill
- **Status**: Completed
- **Learnings & Context**: Implemented testing_harness.py to run the pytest suite natively in python inside the virtual environment. This prevents verbose bash chains like `source .venv/bin/activate && PYTHONPATH=. pytest` from clogging the execution loop. Successfully dogfooded the skill to verify all 9 tests pass.
- **Feedforward Invariants**:
  - `[x] TDD is executed entirely through python testing harness`

## Node 15: Materialize Orthogonal GitHub CI Pipeline
- **Status**: Completed
- **Learnings & Context**: Materialized a pristine GitHub Actions CI pipeline (.github/workflows/python-ci.yml) to serve as a cloud gatekeeper. Documented in WHY-0007 that this cloud layer remains completely decoupled from the Agent's local testing_harness.py skill.
- **Feedforward Invariants**:
  - `[x] GitHub CI runs raw pytest independently of Agent skills`

## Node 16: Establish Pull Request HITL Gate
- **Status**: Completed
- **Learnings & Context**: Successfully transitioned the SPAO loop to a Branch & Pull Request paradigm. Strict branch naming (`node/<id>-<kebab-case>`) is now programmatically enforced via regex in `flow_state_manager.py`. Local hygiene is automated via `sync_and_clean_node`.
- **Feedforward Invariants**:
  - `[x] Agent is paralyzed from advancing to the next node until the Operator merges the PR`

## Node 17: CI Budget Optimization
- **Status**: Completed
- **Learnings & Context**: Removed `pull_request` trigger from GitHub Actions to optimize compute budget. Updated `WHY-0007` to document the decision to rely on local TDD instead of burning cloud minutes on open PRs.
- **Feedforward Invariants**:
  - `[x] GitHub CI only triggers on main pushes`

## Node 18: Materialize Local CI Runner Infrastructure
- **Status**: Completed
- **Learnings & Context**: Successfully established the `infra/` pillar and `infrastructure_state.md`. Built the universal `infra_manager` skill with `systemd_user` routing. Materialized `provision.sh` for the GitHub self-hosted runner and successfully routed CI traffic to it. The runner is active.
- **Feedforward Invariants**:
  - `[x] Infrastructure is formally tracked and agent-controllable`
  - `[x] GitHub CI runs on self-hosted`

## Node 19: Establish Antigravity Hook
- **Status**: Completed
- **Learnings & Context**: Migrated AGENT.md to GEMINI.md to utilize the native Antigravity system prompt hook. Formally codified a Hard Invariant banning raw LLM bash testing, forcing the use of skills/testing_harness.py across all KB documents.
- **Feedforward Invariants**:
  - `[x] Antigravity System reads GEMINI.md automatically`
  - `[x] Native bash testing is forbidden`

## Node 20: Unblock CI Cache Stall
- **Status**: Completed
- **Learnings & Context**: Removed `cache: pip` from `python-ci.yml` because the `actions/setup-python` pip cache synchronization protocol frequently hangs on raw self-hosted runners. A raw pip install takes <2s on the local workstation, rendering the cloud cache redundant anyway.
- **Feedforward Invariants**:
  - `[x] CI Pipeline no longer hangs`

## Node 21: Zero-Network CI Execution
- **Status**: Completed
- **Learnings & Context**: Eliminated all network calls from the CI test step by pre-baking a runner-level venv at ~/actions-runner/venv/. Stripped setup-python and pip install steps from python-ci.yml. The full 16-test suite now executes in 155ms with a 2-step workflow (checkout + pytest). Operator duty for deps refresh is documented in infrastructure_state.md.
- **Feedforward Invariants**:
  - `[x] CI completes in <10s with zero PyPI/CDN calls after checkout`
  - `[x] ci-venv is tracked as a Managed Artifact in infrastructure_state.md`
  - `[x] provision.sh is idempotent and bootstraps the venv on first run`

## Node 22: GitHub Native Backlog Primitives
- **Status**: Completed
- **Learnings & Context**: Established GitHub Issues as the native agentic backlog. Added list_issues_by_label() and add_to_backlog() to github_client.py. Updated sync_and_clean_node() to surface backlog items at every Sense phase. Codified pull convention in HOW-0001. Created the backlog label on GitHub. 19/19 tests pass.
- **Feedforward Invariants**:
  - `[x] Agent can add items to backlog via add_to_backlog()`
  - `[x] Agent surfaces backlog at every Sense phase via sync_and_clean_node()`
  - `[x] Backlog pull convention is codified in HOW-0001`

## Node 27: Materialize GLOSSARY.md
- **Status**: Completed
- **Learnings & Context**: Materialized the authoritative kb/GLOSSARY.md dictionary, defining Node, Spike, Epic, Side-bar, Materialization Boundary, SPAO Loop, HITL, Frontier, Backlog, WIP, Primitive, Feedforward Invariant, and Pillar terms to ensure strict vocabulary consistency across sessions and models.
- **Feedforward Invariants**:
  - `kb/GLOSSARY.md exists`
  - `Terms from seed list are comprehensively defined`

## Node 30: Terminology Synchronization
- **Status**: Completed
- **Learnings & Context**: Successfully synchronized the entire repository with the authoritative GLOSSARY terms. Evaluated and mapped the transition to topological graph theory and SPAO loop terminologies, generated the physical coherence validation artifact, renamed KDR-0001, and updated GEMINI.md, WHAT-0001, HOW-0001, HOW-0002, and historical compliance records to cleanly use "Path" and "Probe".
- **Feedforward Invariants**:
  - `All active files in kb/ and root use Path/Probe`
  - `Coherence Validation artifact exists`
  - `PR matches strict branch naming`

## Node 31: Automated Lexical Guard
- **Status**: Completed
- **Learnings & Context**: Implemented a highly robust Automated Lexical Guard unit test that automatically scans all modified, added, renamed, or untracked files in the active git workspace for stale words (epic/spike). Integrates seamlessly into our local TDD test harness, failing loudly if violations occur. Strictly exempts legacy mapping documents (kb/GLOSSARY.md, artifacts/frontier_state.md, artifacts/coherence_validation.md) to preserve historical accuracy.
- **Feedforward Invariants**:
  - `Lexical guard test suite passes cleanly`
  - `Stale vocabulary is completely blocked on all new codebase mutations`

## Node 32: Shell Script Wrappers
- **Status**: Completed
- **Learnings & Context**: Designed, implemented, and thoroughly tested robust executable bash wrappers (bin/run-tests, bin/sync-clean, bin/plan-node, bin/reflect-node) to encapsulate raw python3 commands. This allows the human operator to tightly whitelist agentic commands in their terminal guardrails without having to generally whitelist python3. Updated all active operational documentation in GEMINI.md and kb/HOW-0001 to point exclusively to the wrapper scripts.
- **Feedforward Invariants**:
  - `All agentic python3 commands successfully wrapped in bin/`
  - `bin/* is fully executable and handles arguments transparently`
  - `Tests verify wrappers execute correctly and prevent recursive test loops`
  - `Operational documents strictly use wrapper commands`

## Node 33: Backlog CLI Abstractions
- **Status**: Completed
- **Learnings & Context**: Materialized precise executable backlog script wrappers (bin/backlog-new, bin/backlog-list, bin/backlog-view, bin/backlog-edit) in the git index with executable permissions (mode 100755), eliminating raw gh calls and permitting secure operator whitelisting. Full TDD subprocess unit testing implemented and verified green.
- **Feedforward Invariants**:
  - `[x] bin/backlog-new, bin/backlog-list, bin/backlog-view, bin/backlog-edit are fully functional`
  - `[x] Full TDD unit test coverage in tests/test_bash_wrappers.py`

## Node 34: Consolidated Backlog CLI
- **Status**: Completed
- **Learnings & Context**: Consolidated multiple separate backlog CLI wrapper scripts into a single unified bin/backlog wrapper script supporting list, new, view, and edit subcommands. This reduces directory clutter, eliminates redundant environment resolver code, and simplifies whitelisting.
- **Feedforward Invariants**:
  - `[x] bin/backlog is fully functional supporting list, new, view, edit`
  - `[x] Full TDD unit test coverage in tests/test_bash_wrappers.py`

## Node 35: Verbose SPAO Stage Tracking
- **Status**: Completed
- **Learnings & Context**: Implemented operator-triggered verbose mode for SPAO loop stage tracking to keep the human operator perfectly aligned and informed of all state transitions and invariant assertions. Verified fully functional with TDD unit tests.
- **Feedforward Invariants**:
  - `[x] SPAO_VERBOSE=1 triggers detailed stage logging banners`
  - `[x] Standard non-verbose execution remains completely silent`
  - `[x] Full TDD unit test coverage in tests/test_flow_state_manager.py`

## Node 36: Terminology Disambiguation
- **Status**: Completed
- **Learnings & Context**: Clarified the ontological definitions and relationships between Loop, Flow, and Path across GLOSSARY.md and WHAT-0001-agentic-architecture.md to prevent cognitive and terminological drift.
- **Feedforward Invariants**:
  - `[x] GLOSSARY.md explicitly distinguishes Loop, Flow, and Path`
  - `[x] WHAT-0001-agentic-architecture.md defines the relationship between Flow and Path`

## Node 37: Ontology - Meta-Tracker Integration
- **Status**: Completed
- **Learnings & Context**: Refined the repository ontology to capture the hierarchies between the Application Tier and the Metasystem Tier, clearly defining recursive 'Meta-' components (Meta-Graph, Meta-Tracker, Meta-Index, Meta-Loop) and anchoring them around Graph and SPAO loop concepts.
- **Feedforward Invariants**:
  - `[x] GLOSSARY.md defines Hierarchical Differentiation and recursive Meta-prefix rules`
  - `[x] GLOSSARY.md defines Meta-Tracker and integrates it into the taxonomy`
  - `[x] WHAT-0001-agentic-architecture.md aligns Section 3.1 and Section 5 with Meta-Tracker taxonomy`

## Node 38: Refactor - Consolidate Node Wrappers
- **Status**: Completed
- **Learnings & Context**: Consolidated distinct bash wrapper entry points bin/plan-node and bin/reflect-node into a single unified bin/node script with plan and reflect subcommands.
- **Feedforward Invariants**:
  - `[x] bin/node implements plan and reflect subcommands`
  - `[x] bin/plan-node and bin/reflect-node are deleted`
  - `[x] tests/test_bash_wrappers.py validates bin/node arguments and usage`

## Node 39: Feature - Meta-Management CLI Integration
- **Status**: [///] Act Phase
- **Learnings & Context**: Implemented a unified bin/meta script to automate Metasystem-level state operations, standardizing our execution transitions and eliminating manual python scripting during the Plan and Reflect phases.
- **Feedforward Invariants**:
  - `[ ] bin/meta implements link, check, and active subcommands`
  - `[ ] skills/frontier_editor.py supports dynamic append_active_node template generation`
  - `[ ] tests/test_bash_wrappers.py validates bin/meta arguments and usage`

## Node 40: Ontology - Multi-Layered SPAO, NC Invariance, and Tiered WIP
- **Status**: [///] Act Phase
- **Learnings & Context**: Codified four canonical GLOSSARY corrections: SPAO universality, NL (Node-Loop), PML (Pre-Materialization Loop), NC (Node Contract), and tiered WIP-N/WIP-P replacing flat WIP=1.
- **Feedforward Invariants**:
  - `[ ] GLOSSARY.md corrects SPAO as universal protocol and introduces NL, PML, NC, WIP-N, WIP-P`
  - `[ ] GLOSSARY.md extends Node definition with mandatory structural attributes`
  - `[ ] WHAT-0001-agentic-architecture.md reflects the two-tier SPAO model`

## Node 41: Probe - Skill vs. Workflow Boundary & bin/ Classification
- **Status**: Completed
- **Learnings & Context**: Evaluated and formally resolved the Skill vs. Workflow boundary, identified flow_state_manager.py as a misclassified Workflow, and classified bin/ as the CLI Adapter Layer.
- **Feedforward Invariants**:
  - `[x] WHY-0009 Decision Record codifies Skill/Workflow boundary and bin/ classification`
  - `[x] GLOSSARY.md adds canonical Skill and Workflow definitions`
  - `[x] WHAT-0001-agentic-architecture.md adds bin/ as CLI Adapter Layer pillar`

## Node 42: Migrate flow_state_manager Workflow
- **Status**: Completed
- **Learnings & Context**: Successfully migrated skills/flow_state_manager.py to orchestrator/flow_state_manager.py, correcting its misclassification as per WHY-0009. Updated all imports in bin/ scripts and tests/ and confirmed 100% test passage.
- **Feedforward Invariants**:
  - `[x] flow_state_manager.py exists in orchestrator/`
  - `[x] all bin scripts import from orchestrator`
  - `[x] all tests pass`

## Node 43: Decouple testing_harness Skill
- **Status**: Completed
- **Learnings & Context**: Stripped SPAO stage awareness from testing_harness.py and moved logging to bin/run-tests. Acknowledged backlog creation invariant violation.
- **Feedforward Invariants**:
  - `[x] log_stage_advancement removed from testing_harness.py`
  - `[x] log_stage_advancement added to bin/run-tests`
  - `[x] tests pass`

## Node 44: Enforce node plan Edit-Only Guardrail
- **Status**: Completed
- **Learnings & Context**: Modified orchestrator/flow_state_manager.py and bin/node to enforce that plan_node strictly takes an existing Backlog Issue ID instead of creating a new issue, ensuring all new nodes originate from the backlog. Updated tests and HOW-0001.
- **Feedforward Invariants**:
  - `[x] flow_state_manager.py updated`
  - `[x] bin/node updated`
  - `[x] HOW-0001 updated`
  - `[x] tests updated and pass`

## Node 45: Evaluate Meta-Rules Reference Pattern
- **Status**: Completed
- **Learnings & Context**: Expanded GEMINI.md to include Section 5: Meta-Rules & Guardrails index, enforcing strict system invariants directly in the System Prompt Hook instead of creating a fragmented rules/ directory.
- **Feedforward Invariants**:
  - `[x] GEMINI.md updated with Rules section`

## Node 46: Establish Repository .gitignore
- **Status**: Completed
- **Learnings & Context**: Created .gitignore at the repository root and purged .venv, .pytest_cache, and __pycache__ from git tracking. The index now correctly ignores these dynamic files, fixing the git pull sync-clean conflict.
- **Feedforward Invariants**:
  - `[x] .gitignore created`
  - `[x] __pycache__ untracked`
  - `[x] .venv untracked`
  - `[x] tests pass`

## Node 28: Issue Factory Skill
- **Status**: Completed
- **Learnings & Context**: Introduced Issue Factory skill to eliminate inline markdown generation for GitHub Issues. All bodies (Backlog and Contracts) are now generated via strict Operator-editable templates in kb/templates/. Enforced template usage in HOW-0001.
- **Feedforward Invariants**:
  - `[x] kb/templates created`
  - `[x] skills/issue_factory.py created`
  - `[x] HOW-0001 updated`
  - `[x] tests pass`

## Node 47: Abstract GH Issue View CLI
- **Status**: Completed
- **Learnings & Context**: Added the view subcommand to bin/node to provide native, zero-friction payload inspection without breaking adapter encapsulation. bin/backlog view was already implemented.
- **Feedforward Invariants**:
  - `[x] bin/backlog updated`
  - `[x] bin/node updated`
  - `[x] tests updated and pass`

## Node 48: Probe: Architectural Placement of sync-clean (bin/rt)
- **Status**: [///] Plan Phase (Paused for Evaluation)
- **Learnings & Context**: Surfaced backlog Issue #78 via `sync-clean`. Formulated the Node Contract to migrate `bin/sync-clean` to `bin/rt` and linked it to Epic #10. Evaluated whether `rt` should be just a CLI adapter (Option A) or elevated to a core Pillar (Option B). Suspended the node loop to persist state pending operator decision for future pick-up.
- **Feedforward Invariants**:
  - `[ ]` Operator selects Option A or Option B.
  - `[ ]` Node is resumed.

## Node 49: Feature - Refactor backlog-add to use templates
- **Status**: Completed
- **Learnings & Context**: Successfully refactored backlog new to take type, title, and goal, leveraging the backlog_issue template. Also modified plan_node to enforce topological GH title consistency.
- **Feedforward Invariants**:
  - `[x] backlog-add updated`
  - `[x] node plan updated`
  - `[x] tests pass`

## Node 50: Node 50: Probe - Evaluate Node Numbering Scheme
- **Status**: [///] Act Phase
- **Learnings & Context**: Cross-reference options based on industry best practices.
- **Feedforward Invariants**:
  - `[ ] Research best practices`
  - `[ ] Output evaluation`

## Node 84: Feature - Refactor Node ID to match GH Issue ID
- **Status**: Completed
- **Learnings & Context**: Successfully refactored CLI wrappers to drop node_id parameter and implemented Option 4. Tests pass and docs updated.
- **Feedforward Invariants**:
  - `[x] Drop node_id from bin/node`
  - `[x] Drop node_id from bin/meta`
  - `[x] Update HOW and GLOSSARY`

## Node 81: Feature: Refactor backlog-list output format
- **Status**: Completed
- **Learnings & Context**: Refactored backlog list output to natively include the Node ID and stripped legacy node ID prefixes from old backlog items. Fixed argument count bug in meta active.
- **Feedforward Invariants**:
  - `[x] Refactor backlog list`

## Node 89: Feature: Implement Asynchronous Prompt Backlog
- **Status**: Completed
- **Learnings & Context**: Successfully executed the Option A blueprint to establish an asynchronous prompt/signal queue. Built bin/prompt and updated loop mechanics and glossary.
- **Feedforward Invariants**:
  - `[x] Create bin/prompt`
  - `[x] Update HOW-0001`
  - `[x] Update GLOSSARY`

## Node 90: Feature: Inject Node ID during Backlog Creation
- **Status**: Completed
- **Learnings & Context**: Successfully implemented the feature to natively enforce the Hybrid Node ID scheme at the exact moment of GH Issue creation by extracting the generated Issue ID and immediately invoking a rename operation.
- **Feedforward Invariants**:
  - `[x] Update github_client.py`

## Node 95: Activity 95: Audit Node Types against Enum
- **Status**: Completed
- **Learnings & Context**: Successfully enforced a strict node-type validation layer inside bin/backlog to guarantee alignment.
- **Feedforward Invariants**:
  - `[x] Update bin/backlog`

## Node 97: Activity 97: Clean up duplicate formatting in flow_state_manager.py
- **Status**: Completed
- **Learnings & Context**: Successfully removed the redundant `#{}` issue ID formatting from the `sync-clean` pipeline.
- **Feedforward Invariants**:
  - `[x] Update flow_state_manager.py`

## Node 100: Activity 100: Triage and resolve duplicate NodeID and Activity ID
- **Status**: Completed
- **Learnings & Context**: Successfully removed the redundant `Node {id}: ` string interpolation from the ledger update path.
- **Feedforward Invariants**:
  - `[x] Update frontier_editor.py`

## Activity 102: Abstract PR creation command sequence for node completion
- **Status**: Completed
- **Learnings & Context**: Implemented create_pull_request in github_client.py and repaired the reflect_node git abstraction sequence.
- **Feedforward Invariants**:
  - `[x] Update github_client.py`
  - `[x] Update flow_state_manager.py`
  - `[x] Close Probe 92`

## Probe 98: Architectural Evaluation of mgr-* Orchestrators
- **Status**: Completed
- **Learnings & Context**: Completed architectural evaluation. Updated WHAT-0001 to document the new CLI Router layer architecture and spawned Activity 104 to formally execute the migration.
- **Feedforward Invariants**:
  - `[x] Draft implementation plan`
  - `[x] Update WHAT-0001`
  - `[x] Spawn execution node`

## Activity 106: Automate PR title injection in reflect_node
- **Status**: Completed
- **Learnings & Context**: Stripped the manual pr_title arg from the CLI and orchestrator layers to eliminate double-prefixing.
- **Feedforward Invariants**:
  - `[x] Update bin/node`
  - `[x] Update flow_state_manager.py`
  - `[x] Update test suite`

## Activity 108: Refactor prompt backlog to YAML
- **Status**: Completed
- **Learnings & Context**: Migrated markdown prompt list to structured YAML pipeline
- **Feedforward Invariants**:
  - `All prompts must maintain status tracking`

## Activity 113: List items in prompt queue
- **Status**: Completed
- **Learnings & Context**: Abstracted shell wrapper logic into formal mgr_prompt python module
- **Feedforward Invariants**:
  - `All CLI domains must be backed by a native mgr-* orchestrator`

## Activity 109: Link consumed prompts to PR bodies
- **Status**: Completed
- **Learnings & Context**: Integrated mgr_prompt into reflect phase to automatically trace and consume prompts from the YAML backlog.
- **Feedforward Invariants**:
  - `All consumed prompts must map to a PR body`

## Probe 125: Architectural Evaluation of Hot-Fix Workflow
- **Status**: Completed
- **Learnings & Context**: Concluded that a Tiered Governance Model is needed. Trivial documentation changes warrant a formalized bin/hotfix tool rather than the heavy SPAO overhead, provided they are logged to a lightweight ledger to prevent traceability loss.
- **Feedforward Invariants**:
  - `Direct commits to main are forbidden without using the bin/hotfix tool`
  - `which mandates traceability.`

## Activity 127: Implement bin/rt formal primitive
- **Status**: Completed
- **Learnings & Context**: Created mgr_rt.py orchestrator and bin/rt adapter. Learned that git push origin main from a feature branch pushes the local main, not the checked-out branch, requiring strict branch verification.
- **Feedforward Invariants**:
  - `Hot-fixes must strictly execute only on the main branch to prevent cross-branch contamination`

## Activity 124: Add prompt-processing hook into GEMINI.md SPAO instructions
- **Status**: Completed
- **Learnings & Context**: Explicitly updated GEMINI.md to require agents to run ./bin/prompt list to check and process the queue, and then to consume them in reflect.
- **Feedforward Invariants**:
  - `[x] GEMINI.md explicitly requires prompt queue processing`

## Activity 122: Implement file-locking mechanism for shared artifacts
- **Status**: Completed
- **Learnings & Context**: Implemented a reentrant cross-platform advisory file-locking mechanism in skills/file_locker.py using fcntl and threading.local. Wrapped all reads and writes to shared artifacts (frontier_state, prompt_backlog, hotfix_ledger) to ensure orthogonal thread safety.
- **Feedforward Invariants**:
  - `[x] file_locker implemented and integrated into shared artifacts`

## Activity 121: Implement git worktree management for orthogonal parallelism
- **Status**: Completed
- **Learnings & Context**: Implemented checkout subcommand in bin/node and flow_state_manager to automatically provision isolated git worktrees inside .worktrees/ directory. Also fixed the reflect_node commit sequence to ensure consumed prompts are properly synced and traceability is maintained.
- **Feedforward Invariants**:
  - `[x] bin/node supports checkout and provisions worktrees`
  - `[x] prompt queue consumption bug fixed with a 2-commit strategy`

## Activity 134: Implement universal --help and -h support for all bin/ CLI adapters
- **Status**: Completed
- **Learnings & Context**: Successfully implemented universal --help and -h parsing blocks for all 7 bin/ scripts, standardizing CLI help output and fulfilling the prompt requests.
- **Feedforward Invariants**:
  - `All bin/ scripts gracefully handle --help and exit 0`
  - `Test suite maintains 100% pass rate`

## Activity 136: Execute Architectural Migration of sync-clean to bin/node sync
- **Status**: Completed
- **Learnings & Context**: Successfully migrated the legacy `sync-clean` primitive into the canonical `bin/node` wrapper as the `sync` subcommand. This aligns workspace cleaning perfectly with the node abstraction lifecycle (sync, plan, checkout, reflect, view).
- **Feedforward Invariants**:
  - `bin/sync-clean has been permanently deleted`
  - `bin/node sync invokes the workspace synchronization loop`
  - `Test suite maintains 100% pass rate`

## Activity 137: Implement prompt delete CLI command
- **Status**: Completed
- **Learnings & Context**: Successfully implemented prompt delete CLI command with interactive confirmation. Removed the test prompt from the backlog as requested.
- **Feedforward Invariants**:
  - `Prompt deletion is gated by CLI confirmation`
  - `CLI usage instructions are updated`

## Activity 140: Implement Architectural TTY Hard-Gate
- **Status**: Completed
- **Learnings & Context**: Successfully implemented the TTY Isolation Principle via skills/tty_gate.py. Tested piped bypass prevention successfully. It intercepts any automated inputs and enforces true HITL.
- **Feedforward Invariants**:
  - `TTY Isolation Principle mathematically prevents pipe spoofing`

## Activity 143: Implement prompt clean CLI command
- **Status**: Completed
- **Learnings & Context**: Successfully implemented the bin/prompt clean feature. It purges all consumed prompts non-interactively to facilitate automated maintenance.
- **Feedforward Invariants**:
  - `Added clean_prompts function in mgr_prompt.py`
  - `Registered clean subcommand in argparse and bin/prompt adapter`
  - `Verified that consumed prompts are permanently removed from the yaml file`

## Activity 146: Add meta-rule to GEMINI for gh issue mapping
- **Status**: Completed
- **Learnings & Context**: Mapped gh issue list and view to backlog list and node view respectively
- **Feedforward Invariants**:
  - `[x] GEMINI.md updated`

## Activity 145: Implement GitHub Label-Based Node Locking
- **Status**: Completed
- **Learnings & Context**: Implemented a highly robust atomic distributed lock leveraging GitHub's Label API (`status: in-progress`). The Node Checkout phase now checks the GH API before mutating the filesystem, raising a mathematical invariant if another thread is already working on the Node. This prevents all future parallel merge conflicts related to orthogonal identical-node checkout.
- **Feedforward Invariants**:
  - `checkout_node applies 'status: in-progress' label`
  - `checkout_node aborts if 'status: in-progress' is present`
  - `Test suite maintains 100% pass rate`

## Probe 149: Triage GitHub API Eventual Consistency on Issue State
- **Status**: Completed
- **Learnings & Context**: Identified the root cause of ghost-state backlog collisions as the architectural lag between GitHub's strongly-consistent Issues API and its eventually-consistent Search API. Formulated a mitigation strategy to double-verify issue states using direct Issue API lookups, and generated Activity 150 to implement the patch in `github_client.py`.
- **Feedforward Invariants**:
  - `Probe must not mutate functional logic`
  - `gh issue list (Search API) is eventually consistent`
  - `gh issue view (Issue API) is strongly consistent`

## Activity 150: Mitigate GitHub API Eventual Consistency
- **Status**: Completed
- **Learnings & Context**: Implemented a double-verification pattern in `list_issues_by_label`. The system now fetches issues via the eventually-consistent Search API (`gh issue list`) and cross-verifies each issue's state using the strongly-consistent Issues API (`gh issue view`). This mathematically eliminates the ghost-state bug where closed issues momentarily reappear in the backlog.
- **Feedforward Invariants**:
  - `list_issues_by_label cross-verifies state with Issues API`
  - `Test suite maintains 100% pass rate`

## Activity 154: Add invariant check for closed PR before branch cleanup
- **Status**: Completed
- **Learnings & Context**: Implemented WIP-N=1 invariant check by querying GitHub API for open PRs before proceeding with SENSE phase sync and cleanup.
- **Feedforward Invariants**:
  - `sync_and_clean_node queries GitHub API for open PRs`
  - `Raises Exception if PRs are open`
  - `Test suite maintains 100% pass rate`

## Probe 153: Architectural Evaluation of Terminal vs Non-Terminal Node Abstraction
- **Status**: Completed
- **Learnings & Context**: Evaluated the benefit of abstracting nodes into Terminal (execution, leaf) and Non-Terminal (composite, path) base classes. This purely graph-theoretic abstraction decouples the Antigravity orchestration logic from the software development domain, allowing generic reuse across arbitrary domains like `agent-travel`. Queued Activity 156 to formally implement this abstraction.
- **Feedforward Invariants**:
  - `Probe must not mutate functional logic`
  - `Terminal Node represents leaf/execution node`
  - `Non-Terminal Node represents composite/parent node`

## Node 157: Implement Soft-Locking for Node Checkout
- **Status**: Completed
- **Learnings & Context**: Implemented a soft-lock in flow_state_manager to emit a yellow warning instead of raising an exception. Preserved the backlog label to ensure visibility. Captured the architectural decision in WHY-0011.
- **Feedforward Invariants**:
  - `[x] checkout_node acts as a soft-lock`
  - `[x] backlog label is preserved`
  - `[x] tests pass`

## Probe 159: Evaluate node plan-start and plan-finish commands
- **Status**: Completed
- **Learnings & Context**: Determined that planning must be a stateful, two-step protocol (`plan-start` and `plan-finish`) to prevent race conditions during prolonged multi-turn drafting sessions. `plan-start` acts as the immediate GH Label lock, while `plan-finish` finalizes the contract. This definitively hardens the SPAO WIP-N=1 invariant against parallel agentic collisions.
- **Feedforward Invariants**:
  - `Probe must not mutate functional logic`
  - `plan-start applies status: in-progress lock immediately`
  - `plan-finish uploads final contract to Issue body`

## Node 163: Probe 163: Audit State Inconsistencies
- **Status**: Completed
- **Learnings & Context**: Executed the trivial inline remediation for Node 163. Synchronized the Epic Meta-Index (Issue #10) to include all historical nodes up to Node 161. Corrected the active node pointer in `frontier_state.md` and finalized the `0002-state-inconsistencies.md` audit payload.
- **Feedforward Invariants**:
  - `Epic Meta-Index must track all completed nodes`
  - `Active Node pointer in frontier_state.md must be accurate`
  - `Audit payloads must be materialized in artifacts/audit`

## Activity 161: Implement Multi-Phase Node Planning (plan-start and plan-finish)
- **Status**: Completed
- **Learnings & Context**: Successfully decomposed `bin/node plan` into `plan-start` (which acquires the GitHub label lock immediately) and `plan-finish` (which finalizes the contract). This architectural shift guarantees that the WIP-N=1 invariant is preserved even during protracted agentic planning and drafting phases. `checkout` has been updated to safely inherit the lock idempotently.
- **Feedforward Invariants**:
  - `bin/node plan is replaced by plan-start and plan-finish`
  - `plan-start acquires status: in-progress immediately`
  - `checkout applies lock idempotently without fatal exception`

## Audit State Inconsistencies
- **Status**: Completed
- **Learnings & Context**: Successfully audited and corrected stale frontier_state and Epic Meta-Index missing items.
- **Feedforward Invariants**:
  - `State invariants have been restored.`

## Activity 167: allow manual triggering to process prompts-queue
- **Status**: Completed
- **Learnings & Context**: Implemented the process subcommand for bin/prompt to allow manual consumption of prompts.
- **Feedforward Invariants**:
  - `[x] Process logic implemented in mgr_prompt.py`
  - `[x] bin/prompt wrapper updated`

## Codify Manager and Dual-Agent Ontology
- **Status**: Completed
- **Learnings & Context**: Established the formal mathematical decoupling of Workflow from Agent, codified the concept of a Manager, and asserted the Dual-Agent (Operator/Auditor) paradigm for true system autonomy.
- **Feedforward Invariants**:
  - `All future architectural references must align with the Manager = Agent + Workflow paradigm.`

## Activity 171: Node internal lifecycle and workflow management
- **Status**: Completed
- **Learnings & Context**: Created orchestrator/node_lifecycle.py with BaseNode and TerminalNode classes, migrating procedural SPAO logic into TerminalNode. Refactored flow_state_manager to act as an adapter layer delegating to TerminalNode instances. This establishes the OOP foundation. Also Resolves #156.
- **Feedforward Invariants**:
  - `[x] Node SPAO lifecycle is object-oriented`
  - `[x] Abstract BaseNode and TerminalNode created`

## Abstract Nodes into Terminal and Non-Terminal Base Classes
- **Status**: Completed
- **Learnings & Context**: Abstracted Node classification into Terminal and Non-Terminal Base Classes via antigravity.yml configuration, unlocking domain portability.
- **Feedforward Invariants**:
  - `All domain-specific Node Taxonomy mappings must be defined in antigravity.yml at the repository root.`

## Execute Architectural Migration of mgr-* Orchestrators
- **Status**: Completed
- **Learnings & Context**: Migrated flow_state_manager.py natively into orchestrator/mgr_node.py to formally establish the Manager pattern. Refactored bin/node as a proxy wrapper and added argparse.
- **Feedforward Invariants**:
  - `Manager components must inherently own their workflows.`

## 116-run-tests-abstraction
- **Status**: Completed
- **Learnings & Context**: Integrated test execution natively into mgr_node to align with domain manager separation of concerns. Fixed a critical bug in testing_harness.py where the exact exit code from pytest was swallowed, replacing capture_output with streaming output.
- **Feedforward Invariants**:
  - `[ ]` None

## Activity 138: Decouple Prompt Lifecycle from PR Merge
- **Status**: Completed
- **Learnings & Context**: Removed consume_prompts and PR linkage entirely. Updated process_prompts to handle consumption definitively based on a resolution context. Cleaned up TerminalNode.reflect logic.
- **Feedforward Invariants**:
  - `[x] Prompt lifecycle decoupled from PRs`
  - `[x] Activity 175 created for Node Clean requirements`

## Activity 175: Implement Node Clean Abstraction
- **Status**: Completed
- **Learnings & Context**: Implemented node clean abstraction to parse merged PRs from GitHub and properly dismantle local git state. Switched to forced branch deletion to handle squash merges.
- **Feedforward Invariants**:
  - `[x] GitHub API queried for merged PRs`
  - `[x] Local branch deletion forced for squash merges`

## Activity 32: Audit Daemon
- **Status**: Completed
- **Learnings & Context**: Implemented a modular Python-based Rules Engine (skills/audit_daemon.py) triggered by a systemd --user timer. Configured via audit_config.yml to support dynamic rules with distinct alert levels (FAILURE vs NOTIFICATION). Added robust mock-based TDD tests.
- **Feedforward Invariants**:
  - `[ ]` None

## Probe 179: Architectural Evaluation of Configurable Operator-Gates
- **Status**: Completed
- **Learnings & Context**: Conducted architectural evaluation of HITL gates, determining that a BaseManager OOP pattern (Option C) guided by modular {domain}-gates.yml configuration files provides the best systemic invariant.
- **Feedforward Invariants**:
  - `- [x] kb/WHY-0012-configurable-operator-gates.md exists`

## Activity 182: Implement HookManager and Configuration Schema
- **Status**: Completed
- **Learnings & Context**: Implemented HookManager in orchestrator/sense_hooks.py to dynamically parse antigravity.yml and execute configurable hooks. Hook abstractions have been integrated into sync_and_clean_node.
- **Feedforward Invariants**:
  - `[x] HookManager dynamically parses configuration`
  - `[x] Sense Phase abstracted into modular execution pattern`

## Activity 187: Implement Prompt Queue Hook
- **Status**: Completed
- **Learnings & Context**: Implemented the execute_prompt_queue_hook function in sense_hooks.py to consume the configurable backlog_file parameter. Updated mgr_prompt.py to support non-default backlog file resolution, enabling dynamic configuration in the HookManager.
- **Feedforward Invariants**:
  - `[x] Prompt Queue hooked into Sense cycle`
  - `[x] mgr_prompt primitives support custom paths`

## Activity 189: Implement Next-Best-Action Skill and Hook
- **Status**: Completed
- **Learnings & Context**: Created skills/nba_evaluator.py as a stateless skill implementing two-tier NBA logic: path continuation (finds pending activities within the active Path) and path switching (falls back to global backlog). Wired into execute_next_best_action_hook in sense_hooks.py.
- **Feedforward Invariants**:
  - `[x] NBA skill is stateless and pure`
  - `[x] Two-tier logic: path continuation and path switching`
  - `[x] Hook consumes NBA skill output`

## Probe 193: Architectural Evaluation of Normalized Status Labels
- **Status**: Completed
- **Learnings & Context**: Investigated and codified the node.yml schema and set_status abstraction in WHY-0013.
- **Feedforward Invariants**:
  - `WHY-0013 exists`
  - `Schema maps logical to physical labels`

## Activity 191: Codify Path Invariant Enforcement
- **Status**: Completed
- **Learnings & Context**: Decoupled Active Path and Active Node in frontier_state.md. Hooked NBA skill into TerminalNode.reflect to automatically assert path closure invariant.
- **Feedforward Invariants**:
  - `[x] Current Active Path and Current Active Node are decoupled in frontier_state.md\n[x] TerminalNode.reflect automatically closes Paths with 0 pending children`

## Activity 194: Implement node.yml Configuration Schema
- **Status**: Completed
- **Learnings & Context**: Created node.yml schema mapped to industry standard statuses and implemented parsing logic in node_lifecycle.py
- **Feedforward Invariants**:
  - `node.yml exists`
  - `load_node_status_config implemented`

## Activity 195: Abstract State Changes to node set-status
- **Status**: Completed
- **Learnings & Context**: Implemented BaseNode set_status and set_classification to map logical statuses to github labels, and exposed them via mgr_node CLI
- **Feedforward Invariants**:
  - `set_status API exists`
  - `bin/node set-status CLI wrapper exists`
  - `Execution layer remains untouched (Node 196)`

## Activity 196: Refactor Node Locking to Use node set-status
- **Status**: Completed
- **Learnings & Context**: Refactored TerminalNode.plan_start and TerminalNode.checkout to use the BaseNode.set_status abstraction instead of hardcoded github labels.
- **Feedforward Invariants**:
  - `TerminalNode uses set_status`
  - `Hardcoded status: in-progress eliminated from orchestrator`

## Probe 203: Refine Intent and Problem Statement for Topological Invariants
- **Status**: Completed
- **Learnings & Context**: Drafted WHY-0014 defining the Orphaned Node Fallacy and Dual-Probe Initialization rule.
- **Feedforward Invariants**:
  - `WHY-0014 exists`

## Probe 204: Scope Necessary Activities for Topological Invariants
- **Status**: Completed
- **Learnings & Context**: Created Activities 206, 207, and 208 to implement the topological invariants.
- **Feedforward Invariants**:
  - `Backlog populated`

## Activity 208: Reopen and Reconstruct Path 202 Meta-Index
- **Status**: Completed
- **Learnings & Context**: Added reopen_issue skill to github_client and reconstructed the Meta-Index payload for Path 202.
- **Feedforward Invariants**:
  - `reopen_issue skill exists`
  - `Path 202 Meta-Index contains 203, 204, 206, 207, 208`

## Activity 207: Enforce --path Constraint on bin/backlog new
- **Status**: Completed
- **Learnings & Context**: Implemented argparse in bin/backlog and refactored add_to_backlog to mathematically link terminal nodes to their parent Path's Meta-Index. Auto-injection logic verified with unit tests.
- **Feedforward Invariants**:
  - `bin/backlog rejects orphaned nodes`
  - `add_to_backlog updates parent body automatically`
  - `tests pass`

## Activity 206: Update Core Ontologies (WHAT-0001 & HOW-0001)
- **Status**: Completed
- **Learnings & Context**: Formally codified the Orphaned Node Fallacy and Dual-Probe Initialization constraints into WHAT-0001 and HOW-0001, permanently establishing these invariants in the system's philosophical ROM.
- **Feedforward Invariants**:
  - `WHAT-0001 updated`
  - `HOW-0001 updated`

## Probe 215: Scope Necessary Activities for Path Execution Guardrails
- **Status**: Completed
- **Learnings & Context**: Scoped out the necessary Activities to enforce orthogonal scopes, pre/post-requisite contracts, and dynamic children traversal order. Generated Activities 223, 224, and 225 and injected them into the Path 213 Meta-Index.
- **Feedforward Invariants**:
  - `Activities 223, 224, 225 generated`

## Probe 214: Refine Intent and Problem Statement for Path Execution Guardrails
- **Status**: Completed
- **Learnings & Context**: Drafted WHY-0015 to formalize orthogonal scope, pre/post-requisite contracts, and dynamic children traversal order. Dog-fooded dynamic traversal by automatically generating a third Probe for Path 213 mid-execution.
- **Feedforward Invariants**:
  - `WHY-0015 exists`
  - `Dog-food Probe generated`

## Probe 215: Scope Necessary Activities for Path Execution Guardrails
- **Status**: Completed
- **Learnings & Context**: Scoped out the necessary Activities to enforce orthogonal scopes, pre/post-requisite contracts, and dynamic children traversal order. Generated Activities 223, 224, and 225 and injected them into the Path 213 Meta-Index.
- **Feedforward Invariants**:
  - `Activities 223, 224, 225 generated`

## Probe 221: Holistic Evaluation of Path Modifications
- **Status**: Completed
- **Learnings & Context**: Identified Graph Traversal Fallacy, Flat-List Fallacy, and Closure Synchronization Bug. Scoped out 3 new Activities to evolve the Meta-Index into a DAG format and refactor the NBA evaluator to parse it dynamically.
- **Feedforward Invariants**:
  - `Activities 227, 228, 229 generated`

## Activity 223: Enforce Contract Sections in Issue Templates
- **Status**: Completed
- **Learnings & Context**: Replaced generic Invariants section with strict Pre-Requisite and Post-Requisite sections in both backlog_issue.md and node_contract.md templates. Updated github_client.py to inject these dependencies correctly during new node generation.
- **Feedforward Invariants**:
  - `Templates updated`
  - `tests pass`

## Activity 227: Evolve Meta-Index into a DAG Syntax
- **Status**: Completed
- **Learnings & Context**: Updated bin/backlog to accept --depends and modified github_client.py to append DAG annotations (e.g., [Depends: 223, 224]) to both the parent Path Meta-Index and the child issue body.
- **Feedforward Invariants**:
  - `CLI accepts --depends`
  - `DAG injection validated`
  - `tests pass`

## Activity 228: Refactor nba_evaluator to parse Meta-Index DAG
- **Status**: Completed
- **Learnings & Context**: Replaced numeric guesswork in nba_evaluator with a native DAG parser that pulls the parent Path's GH issue body, parses all nodes and their dependencies, and mathematically surfaces the unblocked true Next-Best-Actions.
- **Feedforward Invariants**:
  - `DAG parsing implemented`
  - `numeric guessing removed`
  - `tests pass`

## Activity 229: Automate Meta-Index Checkbox Synchronization on Reflect
- **Status**: Completed
- **Learnings & Context**: Added github_client.check_off_meta_index() to automatically swap [ ] with [x] in the parent Path's Meta-Index. Injected this synchronization call directly into TerminalNode.reflect before the nba_evaluator runs, ensuring the DAG parser recognizes the node's completion.
- **Feedforward Invariants**:
  - `Meta-Index checkbox synchronization automated`
  - `tests updated and passing`
  - `Activity 224 manually closed out successfully using this hook`

## Activity 225: Enforce Orthogonal Scope Validation
- **Status**: Completed
- **Learnings & Context**: Implemented Orthogonal Scope Validation guardrail inside TerminalNode.plan_start. This prevents duplicate/overlapping work generation by scanning the backlog for concurrent Activities with identical goals or canonical titles.
- **Feedforward Invariants**:
  - `Orthogonal Scope Validation implemented`
  - `tests updated and passing`

## Probe 238: Formulate the Sense-Gate Invariant Architecture
- **Status**: Completed
- **Learnings & Context**: Formulated the architectural rationale for the two-pronged Sense-Gate in kb/WHY-0013-sense-phase-operator-gate.md. This establishes the requirement for both Behavioral (Meta-Instruction) and Environmental (CLI warning) gates to prevent autonomous SENSE -> PLAN transitions.
- **Feedforward Invariants**:
  - `Sense-Gate architecture formalized`
  - `Two-pronged enforcement strategy documented`

## Activity 239: Codify the Sense-Gate Invariant
- **Status**: Completed
- **Learnings & Context**: Implemented the behavioral and environmental gates to explicitly operator-gate the Sense Phase. Updated GEMINI.md and HOW-0001 with The Sense-Gate Invariant. Injected ANSI-colored warning into nba_evaluator.py.
- **Feedforward Invariants**:
  - `Sense-Gate Invariant added to GEMINI.md`
  - `Environmental warning added to nba_evaluator`
  - `tests pass`

## Probe 243: Evaluate Refactoring and Promotion of NBA Evaluator
- **Status**: Completed
- **Learnings & Context**: Successfully analyzed the current implementation, drafted an architectural promotion strategy, and spawned execution Activities 244-247. Decisions codified in WHY-0016.
- **Feedforward Invariants**:
  - `WHY-0016 exists`
  - `Meta-Index updated`

## Implement gh_graph_skill.py stateless primitive
- **Status**: Completed
- **Learnings & Context**: Successfully extracted graph-parsing logic from nba_evaluator.py into a dedicated, stateless skill gh_graph_skill.py. Verified with 100% test coverage (87/87 tests passed).
- **Feedforward Invariants**:
  - `gh_graph_skill.py implemented`
  - `nba_evaluator.py refactored`
  - `tests pass`

## Hardened Meta-Index traceability and implemented bin/meta audit
- **Status**: Completed
- **Learnings & Context**: Meta-Index synchronization is now robust against formatting variations
- **Feedforward Invariants**:
  - `[x] Robust Path ID extraction implemented`
  - `[x] bin/meta audit implemented`
  - `[x] Path labeling fixed`

## Implement NBAManager orchestrator
- **Status**: Completed
- **Learnings & Context**: Successfully migrated high-level navigation logic from legacy skill to a formal orchestrator.
- **Feedforward Invariants**:
  - `[x] NBAManager implemented`
  - `[x] integrated into sense_hooks`
  - `[x] verified with tests and manual execution.`

## Decommission legacy NBA skill and formalize primitive
- **Status**: Completed
- **Learnings & Context**: Successfully promoted NBA to a first-class primitive and refactored the legacy skill into a thin proxy.
- **Feedforward Invariants**:
  - `[x] nba_evaluator.py refactored as proxy`
  - `[x] WHAT-0017 materialized`
  - `[x] WHAT-0001 updated`
  - `[x] obsolete tests deleted.`

## Materialize template-driven NBA banners
- **Status**: Completed
- **Learnings & Context**: Successfully migrated NBA banner rendering to a formal template-driven system with ANSI support.
- **Feedforward Invariants**:
  - `[x] kb/templates/nba_banner.md created`
  - `[x] sense_hooks.py refactored`
  - `[x] tests updated and passed.`

## Verify NBA Orchestrator Accuracy
- **Status**: Completed
- **Learnings & Context**: Successfully verified that the new NBAManager correctly identifies Probe nodes in the backlog, resolving the failures observed in the legacy evaluator.
- **Feedforward Invariants**:
  - `[x] NBAManager verified`
  - `[x] Legacy issues 217-220 closed as resolved.`

## Probe 257: Refine NBA Presentation Requirements
- **Status**: Completed
- **Learnings & Context**: Reordered NBA banner to prioritize Path information with bold styling. Added robust newline handling to Meta-Index parser.
- **Feedforward Invariants**:
  - `[ ]` None

## Probe 258: Scope NBA Presentation Enhancements
- **Status**: Completed
- **Learnings & Context**: Finalized technical scope for semantic color coding, visual framing, and history surfacing.
- **Feedforward Invariants**:
  - `[ ]` None

## Materialize NBA Presentation Enhancements
- **Status**: Completed
- **Learnings & Context**: Implemented framed, color-coded, and history-aware NBA banner.
- **Feedforward Invariants**:
  - `[ ]` None

## Refactor Test Runner & Legacy Proxies
- **Status**: Completed
- **Learnings & Context**: Successfully migrated testing logic to orchestrator/mgr_testing.py and decommissioned skills/nba_evaluator.py and skills/testing_harness.py. Updated node_lifecycle and mgr_node to align with the new ontology.
- **Feedforward Invariants**:
  - `[x] TestManager materialized`
  - `[x] bin/run-tests purified`
  - `[x] Legacy proxies deleted`
  - `[x] Mocks updated in tests`

## Fix ModuleNotFoundError in PR #284
- **Status**: Completed
- **Learnings & Context**: Successfully resolved CI failures by removing stale test files (tests/test_testing_harness.py) and re-applying the Activity 279 refactoring on a clean branch. All 88 tests pass.
- **Feedforward Invariants**:
  - `[x] Stale tests deleted`
  - `[x] Refactoring re-applied`
  - `[x] 88 tests pass`

## Activity 280: Telemetry Decorator
- **Status**: Completed
- **Learnings & Context**: Implemented @record_execution decorator for automated telemetry. Refactored mgr_node and node_lifecycle to use it. Expanded schema for hierarchical reporting.
- **Feedforward Invariants**:
  - `[x] TDD: 91 tests pass`

## Probe: Align - Refinement of Initialization Invariants
- **Status**: Completed
- **Learnings & Context**: Codified the Triple-Node Doctrine in kb/WHY-0020. This supersedes the Dual-Probe pattern.
- **Feedforward Invariants**:
  - `[x] kb/WHY-0020 exists`
  - `[x] Trinity definition aligned`

## Probe: Plan - Technical Integration of Triple-Node Guardrails
- **Status**: Completed
- **Learnings & Context**: Designed the branch-target invariant and the auto-initialization logic for the Triple-Node trinity. Confirmed hard-halt and immediate backlog labeling for trinity nodes.
- **Feedforward Invariants**:
  - `[x] Branch-Target invariant designed`
  - `[x] Triple-Node auto-init designed`
  - `[x] Hard-halt confirmed`
  - `[x] Backlog labeling confirmed`

## Activity: Reflect - Formal Adoption of Triple-Node Doctrine
- **Status**: Completed
- **Learnings & Context**: Implemented auto-initialization and branch-target invariant. Verified trinity spawning and branch guardrails.
- **Feedforward Invariants**:
  - `[x] Trinity auto-init implemented`
  - `[x] Branch-Target invariant implemented`
  - `[x] Governance docs updated`

## Node 317: Probe 317: Align - Metasystem State Hardening
- **Status**: Completed
- **Learnings & Context**: Established the Atomic State Invariant (WHY-0021) and updated the glossary. This doctrine mandates that ledger updates and pointer transitions occur as a single atomic unit.
- **Feedforward Invariants**:
  - `Atomic State Invariant documented in WHY-0021`
  - `Atomic State Invariant added to GLOSSARY.md`

## Node 318: Probe 318: Plan - Metasystem State Hardening
- **Status**: Completed
- **Learnings & Context**: Implemented atomic state transitions in frontier_editor.py and integrated a stale-pointer audit rule into audit_daemon.py. Added mandatory state purity gating to TerminalNode lifecycle methods.
- **Feedforward Invariants**:
  - `Atomic completion and pointer clearing in frontier_editor.py`
  - `State purity verification in TerminalNode lifecycle`
  - `Stale active node detection in audit_daemon.py`
  - `Audit trigger integrated into node sync`

## Node 319: Activity 319: Reflect - Metasystem State Hardening
- **Status**: Completed
- **Learnings & Context**: Completed the Path 316 cycle. Established the Atomic State Invariant and implemented mandatory state-purity guardrails.
- **Feedforward Invariants**:
  - `Metasystem state is now atomic and self-auditing`

## Plan - Regression Testing Architecture Hardening
- **Status**: Completed
- **Learnings & Context**: Implemented centralized test support layer (conftest.py, harness.py) and integrated a mandatory patch-density guardrail into mgr_testing.py. Refactored major test files to comply with orthogonality requirements.
- **Feedforward Invariants**:
  - `Test files MUST NOT exceed 10 patches`
  - `Standardize on pytest fixtures`

## Format active node name with Node id prefix in frontier_editor
- **Status**: Completed
- **Learnings & Context**: Updated skills/frontier_editor.py to format appended active node titles using the Node {id}: prefix, ensuring consistent representation across the frontier state file. Updated tests/test_frontier_editor.py assertions to verify the formatting.
- **Feedforward Invariants**:
  - `Active node titles must include Node id prefix`

## Reflect - Regression Testing Architecture Hardening (Orthogonality & Reuse)
- **Status**: Completed
- **Learnings & Context**: Refactored tests/test_mgr_node.py, tests/test_github_client.py, and tests/test_mgr_backlog.py to replace verbose manual patching with clean pytest fixtures defined in tests/conftest.py. Implemented a Patch Density Auditor in orchestrator/mgr_testing.py running on configuration limits defined in test_config.yml. This successfully reduced regression testing overhead, optimized test execution, and instituted automated governance checks to prevent future @patch bloat. Also verified node prefixing logic in skills/frontier_editor.py.
- **Feedforward Invariants**:
  - `Test mock density remains under configured limit (10 patches/file)`
  - `All tests pass with 100% success rate`
  - `Frontier active nodes are formatted with Node id prefix`

## Node 315: Probe 315: Plan - State Pointer Hardening
- **Status**: Completed
- **Learnings & Context**: Successfully migrated the Metasystem tracking ledger from Markdown to a schema-verified, checksum-verified YAML file (frontier_state.yml). Implemented atomic writes (save state -> rehash -> generate markdown) to prevent pointer corruption. Created bin/meta lint and rehash tools, and integrated a stale-pointer audit rule into audit_daemon.py.
- **Feedforward Invariants**:
  - `[x] Metasystem ledger successfully migrated to YAML format`
  - `[x] Automated state pointer integrity guardrails in place`
  - `[x] Continuous auditing integrated with audit daemon`
  - `[x] Standardized Node prefixing implemented`
  - `[x] All 82 unit and integration tests passing`

## Node 333: Activity 333: De-track Telemetry Log from Git
- **Status**: Completed
- **Learnings & Context**: De-tracked artifacts/telemetry.jsonl from Git tracking to avoid checkout and merge conflicts during node sync operations.
- **Feedforward Invariants**:
  - - '`artifacts/telemetry.jsonl is not tracked in Git`'\n- '`All 82 tests pass cleanly`'\n

## Node 335: Probe 335: Align - Enforce Triple-Node Auto-Initialization for Paths
- **Status**: Completed
- **Learnings & Context**: Aligned on WHY-0022 establishing automated triple-node auto-initialization constraints inside the backlog manager.
- **Feedforward Invariants**:
  - - '`WHY-0022 document created`'\n- '`All 82 tests pass cleanly`'\n

## Node 336: Probe 336: Plan - Enforce Triple-Node Auto-Initialization for Paths
- **Status**: Completed
- **Learnings & Context**: Planned and documented the technical specification for programmatically generating Align Probe, Plan Probe, and Reflect Activity child nodes recursively in BacklogManager.
- **Feedforward Invariants**:
  - - '`WHAT-0023 document created`'\n- '`All 82 tests pass cleanly`'\n

## Node 337: Activity 337: Reflect - Enforce Triple-Node Auto-Initialization for Paths
- **Status**: Completed
- **Learnings & Context**: Implemented recursive automatic triple-node (Align, Plan, Reflect) issue creation in BacklogManager.create for non-terminal paths.
- **Feedforward Invariants**:
  - - '`Paths automatically initialize Align Probe
  - `Plan Probe`
  - and Reflect Activity children`'\n- '`All 83 tests pass cleanly`'\n

## Node 342: Probe 342: Align - Spike Path: Abstraction Doctrine - Python API for git and gh
- **Status**: Completed
- **Learnings & Context**: Aligned on the core requirements of the Abstraction Doctrine, specifying per-concept abstractions for Path/Backlog (consolidated) and Node (internal).
- **Feedforward Invariants**:
  - - '`WHY-0024 decision record created`'\n- '`All 83 tests pass cleanly`'\n

## Node 343: Probe 343: Plan - Spike Path: Abstraction Doctrine - Python API for git and gh
- **Status**: Completed
- **Learnings & Context**: Documented the concrete technical specifications of the Abstraction Doctrine in WHAT-0025, detailing Git/GitHub wrappers, path/backlog consolidation evaluation, and node internality.
- **Feedforward Invariants**:
  - - '`WHAT-0025 specification created`'\n- '`All 83 tests pass cleanly`'\n

## Node 344: Activity 344: Reflect - Spike Path: Abstraction Doctrine - Python API for git and gh
- **Status**: Completed
- **Learnings & Context**: Implemented skills/git_client.py wrapping all git commands in safe subprocess functions. Refactored orchestrator/node_lifecycle.py and orchestrator/mgr_rt.py to call git_client instead of direct CLI subprocess execution, and verified execution via test suite.
- **Feedforward Invariants**:
  - - '`skills/git_client.py wraps add
  - `commit`
  - `push`
  - `restore`
  - `worktree_add`
  - `worktree_remove`
  - `get_current_branch`
  - `get_commit_hash`
  - branch_delete`'\n- '`No raw git subprocesses inside orchestrator modules`'\n- '`All 96 tests pass cleanly`'\n

## Implement Abstraction Remediation and Atomic Transactions
- **Status**: Completed
- **Learnings & Context**: Adding git wrappers and a context-manager transaction layer allows rollbacks of Git and GitHub state on failure, avoiding dirty states and compliance violations.
- **Feedforward Invariants**:
  - `Must always use git_client wrapper functions instead of raw subprocess calls to git in all orchestration modules. Must always wrap state transitions in FlowTransaction.`

## Node 356: Probe 356: Align - Path: Global SPAO System Containment, Deployment, and CLI Integration
- **Status**: Completed
- **Learnings & Context**: Aligned on a hybrid symbolic-linkage and Python package architecture to make the SPAO system globally accessible across target projects.
- **Feedforward Invariants**:
  - `All SPAO scripts must distinguish execution path from workspace target path.`

## Node 357: Probe 357: Plan - Path: Global SPAO System Containment, Deployment, and CLI Integration
- **Status**: Completed
- **Learnings & Context**: Documented the technical specification for dynamic path separation, path resolver utility, unified spao CLI command, and the global installation script in WHAT-0029.
- **Feedforward Invariants**:
  - `All SPAO scripts must distinguish execution path from workspace target path.`

## Node 358: Activity 358: Reflect - Path: Global SPAO System Containment, Deployment, and CLI Integration
- **Status**: Completed
- **Learnings & Context**: Implemented dynamic path resolution, refactored all managers to use skills.path_resolver, introduced a global installer script bin/spao-install, and verified functionality using unit tests and manual multi-workspace validation.
- **Feedforward Invariants**:
  - `All SPAO scripts must distinguish execution path from workspace target path.`

## Node 363: Probe 363: Align - Spike Path: SPAO Release Packaging, One-Step Onboarding & CLI Discoverability
- **Status**: Completed
- **Learnings & Context**: Aligned on two decisions: (1) canonical one-step onboarding is a single `curl | bash -s -- --local` command; (2) `run-spao.sh` must print a usage banner on no-args invocation and a `README.spao.md` must be generated alongside it. WHY-0030 materialized and merged via PR #366. Automated reflect rolled back due to `gh pr create` running from wrong CWD — PR created manually from worktree, then issue closed via rollback handler.
- **Feedforward Invariants**:
  - `[x]` WHY-0030 merged to main
  - `[x]` Issue #363 closed
  - `[ ]` Dependency Enforcement gap in mgr_node.py noted for future hardening

## Current Active Path
Path 362: Spike Path: SPAO Release Packaging, One-Step Onboarding & CLI Discoverability

## Current Active Node
None — awaiting Plan node #364 approval
