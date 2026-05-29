# Family Legacy — Domain Dao Digest v0.1

> **Status**: DRAFT — Awaiting Operator Ratification
> **Project**: familyloom.app — Voice-first iOS app for preserving family stories
> **Source Corpus**: ENGINEERING_BEST_PRACTICES.md, BRANCHING_STRATEGY.md, DOCUMENTATION_STANDARDS.md, AGENT_WORKFLOWS.md, CLAUDE.md, PLAN_SLC.md, ARCH.md, BLUE-001/002/003, DR-020–024, PRD.md, BRD.md, TELEMETRY_*.md, pubspec.yaml
> **Extraction Date**: 2026-05-28
> **Rules Extracted**: ~400 | **Rules in Digest**: ~120 (curated for operational relevance)

---

## 1. Project Identity

| Attribute | Value |
|---|---|
| Package Name | `family_legacy` |
| Bundle ID (iOS) | `tech.familyloom.app` |
| Display Name | familyloom |
| iOS Deployment Target | 15.0 |
| Xcode Scheme | `Runner` (Flutter hardcoded — do NOT rename) |
| App Version | 1.1.0+2026051101 |
| Dart SDK | ^3.10.8 |
| Flutter App Root | `src/client/` |
| Backend Stack | Python 3.12 / FastAPI / Docker on Cloud Run (NOT STARTED) |
| Cloud Provider | GCP exclusively |
| Current Phase | SLC (Simple, Lovable, Complete) |
| Platforms | macOS and Linux development; iOS-only deployment in SLC |

---

## 2. Invariants (MUST — Violation causes damage)

### SCM & Git Governance

- **FL-INV-001**: Every PR MUST serve a previously documented Change Request (JOB, SPEC, TC artifact). No ad-hoc PRs.
  _Source: BRANCHING_STRATEGY.md INV-000_

- **FL-INV-002**: All commits on `main` and Support-Branches MUST exist exclusively as the result of an approved PR merge. No direct commits.
  _Source: BRANCHING_STRATEGY.md INV-001_

- **FL-INV-003**: Every hotfix in a Support-Branch MUST be forward-ported to `main` before the CR ticket is closed.
  _Source: BRANCHING_STRATEGY.md INV-002_

- **FL-INV-004**: A single PR MUST encapsulate changes belonging to only one release lifecycle — exclusively Cloud OR exclusively Mobile.
  _Source: BRANCHING_STRATEGY.md INV-004_

- **FL-INV-005**: The repository MUST NOT contain long-lived environment branches (e.g., `qa`, `staging`, `prod`).
  _Source: BRANCHING_STRATEGY.md INV-005_

- **FL-INV-006**: Git history is append-only. Force-push, force-with-lease, amend-on-pushed, rebase-on-pushed, and reset-then-non-FF-push are **PROHIBITED** (Class 1). No in-band approval can override.
  _Source: BRANCHING_STRATEGY.md INV-009, §4.I_

- **FL-INV-007**: Origin branch deletion, archive ref creation, tag deletion/overwrite, and closing load-bearing trackers require explicit Operator approval (Class 2 — Operator-Gated).
  _Source: BRANCHING_STRATEGY.md §4.I_

- **FL-INV-008**: Every active forward branch MUST keep governance-paths (BRANCHING_STRATEGY, ENGINEERING_BEST_PRACTICES, AGENT_WORKFLOWS, DOCUMENTATION_STANDARDS, `.github/workflows/**`, `tools/lint/**`) byte-identical to `main`.
  _Source: BRANCHING_STRATEGY.md INV-007, §4.H_

- **FL-INV-009**: Git tags are reserved exclusively for deployment markers (TestFlight/App Store). Refactors, audits, governance updates MUST NOT receive tags.
  _Source: BRANCHING_STRATEGY.md §2.5_

- **FL-INV-010**: Merged solo branches MUST be decommissioned (worktree removal + local ref deletion + origin ref deletion + orphan-parent rmdir) before wave closure, in the same working session.
  _Source: BRANCHING_STRATEGY.md INV-OH-004, INV-OH-008_

### Privacy & Data Sovereignty

- **FL-INV-011**: User data is siloed per-user, private by default. Family audio recordings NEVER processed by ad networks, analytics, or LLMs without explicit opt-in. No cross-user queries.
  _Source: ARCH.md §5.4_

- **FL-INV-012**: Analytics events MUST NOT contain PII. All LOG and TRK payloads scrubbed of PII before transmission.
  _Source: BLUE-001 ADR-008, BLUE-003 Analytics §4_

- **FL-INV-013**: Sensitive metadata encrypted in Hive (AES-256). Audio in private app sandbox. Upload via TLS 1.3 only.
  _Source: BLUE-001 §3_

### Recording Engine

- **FL-INV-014**: A recording session MUST be fully recoverable after process termination or device restart. Zero data loss. Session state is append-only.
  _Source: ARCH.md §5.2_

- **FL-INV-015**: Recording Engine auto-saves at regular intervals (≤10s). MUST NOT rely solely on stop event. ≥90% audio recoverable on force-kill.
  _Source: BLUE-001 ADR-017_

- **FL-INV-016**: Each question's audio stored as a separate file. Limits crash loss to current question only.
  _Source: BLUE-001 ADR-016_

### Auth & Identity

- **FL-INV-017**: Email/password authentication is an architectural non-starter for SLC. Authentication exclusively via Google and Apple OAuth.
  _Source: ARCH.md §5.3, ADR-006_

- **FL-INV-018**: Email/password is stubbed in UI but MUST NOT be wired to any auth backend.
  _Source: ARCH.md §10_

- **FL-INV-019**: Access denied by default. Every service MUST validate a token before executing operations. Identity MUST be explicitly proven, never inferred.
  _Source: ARCH.md §5.3_

### Offline-First

- **FL-INV-020**: User features MUST be executable regardless of network state. Lack of connectivity MUST NOT block "Start Recording" or "Save Draft."
  _Source: ARCH.md §5.2_

- **FL-INV-021**: Reads always from Local DB. Writes: Local DB first → Background Sync Queue → Remote API.
  _Source: BLUE-001 §4_

### Cloud & Media

- **FL-INV-022**: API containers MUST NEVER directly stream media. All media upload/download via GCS Signed URLs.
  _Source: BLUE-002 §3, ADR-004_

- **FL-INV-023**: Cloud API MUST implement idempotent replay for upload retries from client.
  _Source: BLUE-002 §4_

### Code Quality

- **FL-INV-024**: Runtime guards (`if (!condition) throw`) MUST be used for any condition depending on user input, network response, or SDK return value. `assert()` alone is insufficient for external-input validation.
  _Source: ENGINEERING_BEST_PRACTICES.md §1.1_

- **FL-INV-025**: Production diagnostics MUST route through `AnalyticsService.capture` / PostHog TRK-800 path. `print`, `debugPrint`, and assert-closure idioms are stripped in release and MUST NOT be used.
  _Source: ENGINEERING_BEST_PRACTICES.md §1.5_

- **FL-INV-026**: SDK boundary observability MUST be applied at every SDK boundary — emit TRK-800 events with `error_class` and `error_message` before swallowing exceptions.
  _Source: ENGINEERING_BEST_PRACTICES.md §1.8_

- **FL-INV-027**: Every framework-shaped decision MUST produce an ADR and a TOA (Trade-Off Analysis) matrix before commitment. Default recommendation is "hire" (use existing framework) not "build."
  _Source: ENGINEERING_BEST_PRACTICES.md §9.3_

### Investigation Discipline

- **FL-INV-028**: A LOG investigation MUST land in three separate commits: (1) Hypothesis+method+expected, (2) Raw outcome, (3) Interpretation/decision.
  _Source: ENGINEERING_BEST_PRACTICES.md §6.2_

- **FL-INV-029**: Every SCM job step that mutates shared state MUST verify the premise still holds before executing (pre-flight verify) and MUST be re-runnable without manual repair (idempotency).
  _Source: ENGINEERING_BEST_PRACTICES.md §8.2–§8.3_

### Documentation

- **FL-INV-030**: YAML frontmatter is mandatory with required fields: `title`, `last_updated` (ISO 8601), `review_status` (DRAFT/NOT-REVIEWED/IN-REVIEW/APPROVED/DEPRECATED).
  _Source: DOCUMENTATION_STANDARDS.md §5, §6.3_

- **FL-INV-031**: Exactly one H1 per document. ATX-only headings. No skipped heading levels. No emojis in engineering documents.
  _Source: DOCUMENTATION_STANDARDS.md §5_

- **FL-INV-032**: Requirements MUST be written as declarative statements (imperative requirements PROHIBITED) and MUST be traceable with unique identifier + verification criteria.
  _Source: DOCUMENTATION_STANDARDS.md §3.4, §6.7_

### Multi-PR Coordination

- **FL-INV-033**: Downstream PR `D` cannot land until ALL prerequisites are MERGED AND forward-ported. `D`'s PR body must contain a Dependencies table mapping `(prereq CR-ID, merge SHA, base branch)`.
  _Source: AGENT_WORKFLOWS.md §9_

- **FL-INV-034**: Modifications to critical infrastructure (Identity, Finance, Auth) require explicit Operator "Permission to Edit" on a per-file basis, regardless of CI status.
  _Source: BRANCHING_STRATEGY.md §1_

---

## 3. Conventions (SHOULD — Expected practice)

### Branch Naming

- **FL-CONV-001**: `main` — primary branch.
- **FL-CONV-002**: `client/v<MAJOR>.x` — release family.
- **FL-CONV-003**: `client/v<MAJOR>.<MINOR>.x` — support branch.
- **FL-CONV-004**: `solo/<anchor>/<operator-alias>/<cr-id>-<short-description>` — solo WIP.
- **FL-CONV-005**: `shared/<anchor>/<cr-id>-<short-description>` — shared WIP.
- **FL-CONV-006**: `tba/<anchor>/<short-description>-<YYYY-MM-DD>` — review-pending archive.
- **FL-CONV-007**: `archive/<original-full-ref>` — finalized archive.
  _Source: BRANCHING_STRATEGY.md §2.2_

### Commit Format

- **FL-CONV-008**: Conventional Commits: `<type>(<scope>): <subject>`.
- **FL-CONV-009**: Required trailers: `CR-ID: <PREFIX>-<id>` and `Agent-Mode: <Shadow|Delegated>`.
- **FL-CONV-010**: CR-ID prefix enum (closed-set): JOB, GH, TER, LOG, RR, SOP, FEAT, INFRA, MOD, UXUI, BLUE, DR, ADR, TC-I, TC-U, TC-P.
  _Source: BRANCHING_STRATEGY.md §1 Auditability_

### Tag Format

- **FL-CONV-011**: TestFlight: `v<M>.<N>.<P>-build-<YYYYMMDDNN>`.
- **FL-CONV-012**: App Store: `v<M>.<N>.<P>`.
  _Source: BRANCHING_STRATEGY.md §4.G3_

### Testing

- **FL-CONV-013**: Test naming: `TC-U-{SPEC_ID}_{description}_test.dart` (unit), `TC-I-{SPEC_ID}_{description}_test.dart` (integration).
  _Source: test/ and integration_test/ directories, CLAUDE.md_

- **FL-CONV-014**: Mocking: Mocktail for new code (ADR-019). Mockito only in legacy files.
  _Source: CLAUDE.md, BLUE-001 ADR-019_

- **FL-CONV-015**: Shared mocks in `test/utils/test_helpers.dart`. Inline mocks only for narrowly-scoped one-off behavior.
  _Source: DR-022_

- **FL-CONV-016**: Strict TDD for build workflow: Red (test MUST fail) → Green (minimal implementation) → Refactor → Verify (MUST pass). STOP if any tests fail.
  _Source: .agent/workflows/build_client.md_

- **FL-CONV-017**: Integration test identity format: `E2E_{TC_ID}_{timestamp}` for `distinct_id`.
  _Source: BLUE-003 Analytics ADR_

### Analytics

- **FL-CONV-018**: `EventConstants.dart` is the single-source-of-truth for event names/property keys. All emission sites MUST reference constants, not string literals.
  _Source: DR-020_

- **FL-CONV-019**: Property-key convention: `snake_case`.
  _Source: DR-020 §2_

- **FL-CONV-020**: Use `$test_mode` exclusively for synthetic data filtering (not custom `is_test_data`).
  _Source: BLUE-003 Analytics ADR_

- **FL-CONV-021**: Super Properties via `register()` — runtime context never passed into individual `capture()` calls.
  _Source: BLUE-003 Analytics §2_

### Content

- **FL-CONV-022**: CMS content path: `src/services/cms/content/`. Content bundled from `src/services/cms/content/v1` into client binary.
  _Source: PLAN_SLC.md, PRD §3.4_

- **FL-CONV-023**: Audio storage path: `Documents/session_{sessionId}_q{questionIndex}.m4a`.
  _Source: PLAN_SLC.md_

- **FL-CONV-024**: Export naming: `[Storyteller]-[Theme]-[Date].mp3`.
  _Source: PRD §3.1_

### Platform Detection

- **FL-CONV-025**: Project developed across macOS and Linux. If platform unclear, ASK before running platform-specific commands. iOS builds, Xcode, xcrun, CocoaPods are macOS-ONLY.
  _Source: CLAUDE.md_

### Agent Workflow

- **FL-CONV-026**: For content creation, use Draft Canvas (markdown scratchpad) first. Do NOT create JSON immediately. Get user approval before generating.
  _Source: .agent/workflows/create_content.md_

- **FL-CONV-027**: Git identity check before publishing. PROMPT user to configure if missing. Do NOT auto-generate identity.
  _Source: .agent/workflows/publish_content.md_

### Documentation

- **FL-CONV-028**: 5-folder SPDLC taxonomy: `1_discovery`, `2_definition`, `3_development`, `4_validation`, `5_operations`.
  _Source: PLAN_SLC.md, DOCUMENTATION_STANDARDS.md_

- **FL-CONV-029**: All engineering docs use RFC 2119 terminology. Pandoc Markdown compliant. English-only, UTF-8.
  _Source: DOCUMENTATION_STANDARDS.md §3.1, §5, §10.1_

- **FL-CONV-030**: ADRs follow standard template: Title, Status (Proposed/Accepted/Superseded/Deprecated/Rejected), Context, Decision, Consequences.
  _Source: DOCUMENTATION_STANDARDS.md §8.2_

### SCM Forward-Port

- **FL-CONV-031**: FP commit message: `docs(<domain>): FP <subject> main → client/v<N>.x (<source-CR-ID>)`. Include `CR-ID:` + `Cross-Domain-Scope:` trailers.
  _Source: AGENT_WORKFLOWS.md §11_

- **FL-CONV-032**: Auto-merge FP PRs when all 5 CI gates green + `mergeable: MERGEABLE`. Operator attention reserved for conflict cases.
  _Source: AGENT_WORKFLOWS.md §11 per §4.H7_

---

## 4. Anti-Patterns (MUST NOT — Explicitly forbidden)

- **FL-AP-001**: `assert(x != null)` followed by `x!` — assert is stripped in release; the `!` then crashes opaquely with no diagnostic context.
  _Source: ENGINEERING_BEST_PRACTICES.md §1.4_

- **FL-AP-002**: Jumping to a fix without structured investigation (LOG artifact) when cause is not obvious from a single read.
  _Source: ENGINEERING_BEST_PRACTICES.md §6_

- **FL-AP-003**: Running investigation steps "to see if it works" — confirmation bias. Design each phase to disprove a hypothesis.
  _Source: ENGINEERING_BEST_PRACTICES.md §6.3_

- **FL-AP-004**: Using `git push --force` or any Class 1 prohibited operation. Ever.
  _Source: BRANCHING_STRATEGY.md §4.I, INV-009_

- **FL-AP-005**: Dedicated `cloud/` release branches — `main` serves as the exclusive cloud branch.
  _Source: BRANCHING_STRATEGY.md §2.1_

- **FL-AP-006**: Hardcoding identifiers and API keys in domain logic. Use environment injection.
  _Source: ENGINEERING_BEST_PRACTICES.md §3_

- **FL-AP-007**: Combining `gh pr merge --squash --delete-branch` when the local branch has an active worktree attached. Use atomic cleanup (INV-OH-008) instead.
  _Source: AGENT_WORKFLOWS.md §11_

- **FL-AP-008**: `cd` into a worktree that may be removed by a later iteration in cleanup loops. Always `cd` to repo root first.
  _Source: AGENT_WORKFLOWS.md §10_

- **FL-AP-009**: Using `noSuchMethod` fallbacks in integration tests. Mocktail forces explicit `when()` stubs.
  _Source: DR-022 §2_

- **FL-AP-010**: Not-Invented-Here (NIH) bias: building in-house when hire-and-customize would be cheaper. 1.5× threshold.
  _Source: ENGINEERING_BEST_PRACTICES.md §9.7_

- **FL-AP-011**: Padding a test case with regression-coverage tests dressed up as RED tests.
  _Source: ENGINEERING_BEST_PRACTICES.md §5.2_

---

## 5. Toolchain

### Client Stack

- **FL-TOOL-001**: Flutter 3.x / Dart 3.x — sole mobile framework.
  _Source: BLUE-001 §1, ADR-001_

- **FL-TOOL-002**: Riverpod (`flutter_riverpod` + code gen) — all state management & DI. All FEAT- logic uses `NotifierProvider`/`ConsumerWidget`.
  _Source: BLUE-001 §2, ADR-013_

- **FL-TOOL-003**: GoRouter — sole routing layer, declarative static tree.
  _Source: BLUE-001 §2, ADR-011_

- **FL-TOOL-004**: Freezed — immutable data models & UI state unions. All MOD- models MUST use Freezed.
  _Source: BLUE-001 ADR-010_

- **FL-TOOL-005**: Drift (SQLite) — sole local persistence. All MOD- schemas as Drift tables.
  _Source: BLUE-001 ADR-003_

- **FL-TOOL-006**: `record` v6.0.0 (capture) + `audioplayers` v5.2.1 (playback) — separate, decoupled audio engines.
  _Source: BLUE-001 ADR-014_

- **FL-TOOL-007**: PostHog (`posthog_flutter` v5.21.0) — single observability SDK (analytics, feature flags, session replays).
  _Source: BLUE-001 ADR-008_

- **FL-TOOL-008**: Mocktail v1.0.4 — sole mocking framework for new code. Mockito v5.4.6 legacy only.
  _Source: BLUE-001 ADR-019_

- **FL-TOOL-009**: Firebase Auth v6.4.0 + Google Sign-In v7.2.0 + Sign in with Apple v7.0.1.
  _Source: pubspec.yaml_

### Backend Stack (Not Yet Implemented)

- **FL-TOOL-010**: Python 3.12 + FastAPI + Docker on Cloud Run (serverless, scale-to-zero).
  _Source: BLUE-002 §1, ADR-002_

- **FL-TOOL-011**: Cloud SQL (PostgreSQL) for relational data. GCS for blob storage.
  _Source: BLUE-002 §1_

- **FL-TOOL-012**: GCS Signed URLs for all media upload/download.
  _Source: BLUE-002 §3, ADR-004_

### CI/CD & Build

- **FL-TOOL-013**: GitHub Actions — exclusive CI/CD. All pipeline logic in `.github/workflows/`.
  _Source: BLUE-003 Ops ADR-002_

- **FL-TOOL-014**: Fastlane + match for iOS deployment automation.
  _Source: BLUE-001 ADR-012_

- **FL-TOOL-015**: Code gen: `dart run build_runner build --delete-conflicting-outputs` for `.mocks.dart`, `.freezed.dart`, `.g.dart`.
  _Source: CLAUDE.md_

### Key Commands

- **FL-TOOL-016**: All `flutter` commands MUST be run from `src/client/`.
- **FL-TOOL-017**: Content asset bundled at `assets/content/all-content.json`.

---

## 6. Architecture Constraints

### Design Patterns

- **FL-ARCH-001**: Clean Architecture (Feature-First): Presentation (Widgets+Notifiers) → Domain (Entities+UseCases) → Data (Repositories+DataSources). Source structure: `lib/src/` as `core/`, `data/`, `domain/`, `infra/`, `ui/`.
  _Source: BLUE-001 §2_

- **FL-ARCH-002**: Hexagonal Architecture (Ports & Adapters) at the global level.
  _Source: ARCH.md §6_

- **FL-ARCH-003**: Repository pattern enforced — no direct DB access from UI.
  _Source: PLAN_SLC.md_

- **FL-ARCH-004**: Coarse-Grained Microservices (cloud): `auth`, `api`, `cms`. Stateless services (state in DB/Redis). Synchronous REST/HTTPS (JSON).
  _Source: BLUE-002 §2_

### Quality Attribute Priority

- **FL-ARCH-005**: 1. Reliability, 2. Security/Privacy, 3. Usability, 4. Performance, 5. Maintainability, 6. Portability.
  _Source: ARCH.md §8_

### SLC Phase Boundaries

- **FL-ARCH-006**: iOS-only. No Android-compatible abstractions in SLC.
  _Source: ARCH.md §10, ADR-005_

- **FL-ARCH-007**: No Family Sharing backend. All data models single-user scoped.
  _Source: ARCH.md §10_

- **FL-ARCH-008**: Budget: $25 one-time + $5/month. Total <$30/month.
  _Source: BRD §2.1_

- **FL-ARCH-009**: Kill-Switch: <50% user engagement post-Session-1 = FAIL.
  _Source: ARCH.md ADR-019_

### Content & Audio

- **FL-ARCH-010**: Hybrid Embedded + API Content Delivery — ship `questions.json` in binary for offline; app checks CMS on launch for delta updates.
  _Source: BLUE-001 ADR-007_

- **FL-ARCH-011**: MP3 at 128 kbps as universal audio format (~1MB/min). Note: current implementation uses M4A — format mismatch is known tech debt.
  _Source: ARCH.md ADR-015, PLAN_SLC.md_

- **FL-ARCH-012**: Exactly one theme per session (enforced via radio button UI).
  _Source: PRD §1.2_

### Analytics Standards

- **FL-ARCH-013**: CloudEvents v1.0 envelope. NDJSON for local files. OpenTelemetry Semantic Conventions for context attributes.
  _Source: BLUE-003 Analytics §1_

- **FL-ARCH-014**: Schema Evolution = Additive Only. New fields use defaults for old clients.
  _Source: BLUE-003 Analytics §2_

### SLOs

- **FL-ARCH-015**: Offline Recording Survival: 100% (no data loss).
- **FL-ARCH-016**: 100% crash recovery (sessions resumable).
- **FL-ARCH-017**: App Launch < 1.5s to "Ready to Interact".
- **FL-ARCH-018**: 60fps (no jank on scroll).
  _Source: ARCH.md §7, BLUE-001 §5_

---

## 7. Agent Operating Boundaries

### Autonomous (No Operator Approval Needed)

- Draft PRs in Shadow mode
- Run unit/widget tests on Linux
- Read/analyze any file in the repository
- Generate code from existing specs
- Lint and validate documentation
- Forward-port governance changes (if all 5 CI gates green + mergeable)

### Operator-Gated (Requires Explicit Approval)

- Merge any PR (unless Delegated mode + clean merge + CI 100%)
- Modify Identity, Finance, or Auth files (per-file "Permission to Edit")
- Delete origin branches or create archive refs (Class 2 operations)
- Create or modify ADRs (requires TOA matrix)
- iOS/Xcode/CocoaPods operations (macOS-only; confirm platform first)
- Content creation (Draft Canvas approval before JSON generation)
- Any destructive shared-state operation

### Forbidden (Agent MUST NOT)

- Force-push, rebase pushed commits, amend pushed commits (Class 1 PROHIBITED)
- Direct commits to `main` or Support-Branches
- Create long-lived environment branches
- Wire email/password auth to any backend
- Process family audio through ad networks, analytics, or LLMs
- Use `print`/`debugPrint` for production diagnostics
- Hardcode API keys or identifiers in domain logic
- Skip structured investigation (LOG) when cause isn't obvious

---

## 8. Current State & Phase Awareness

| Phase | Status | Agent Relevance |
|---|---|---|
| Phase 0: Setup | ✅ Complete (except dev environment) | Low — already done |
| Phase 1: Walking Skeleton | ⏩ Deferred/Superseded | None — skip |
| Phase 2: Mobile Data Layer | 🔄 In Progress (auth = stub) | Medium — auth completion |
| Phase 3: Critical User Flows | ✅ Complete (14 screens) | Low — maintenance only |
| Phase 4: Recording Engine | 🔄 In Progress | Medium — battery warning, background recording missing |
| Phase 5: Cloud Infrastructure | ❌ Not Started | High — backend build opportunity |
| Phase 6: Sync & Cloud Persistence | ❌ Not Started (blocked by Phase 5) | High — blocked |
| Phase 7: Alpha Polish | 🔄 In Progress (~45% alignment) | Medium — content gap (4×3 vs 5×5), UAT |

### Known Tech Debt

- M4A vs MP3 format mismatch (implementation vs spec)
- Last-Write-Wins conflict resolution (edge-case data loss)
- Single-user data model (no multi-user permissions)
- TRK-021 through TRK-028 defined but never called (dead analytics code)
- Duplicate `checklist.complete` event from two screens
- Placeholder PostHog API key (`phc_placeholder_dev_key`)
- No test/prod PostHog separation

---

## Appendix: Source Document Reference

| Document | Size | Primary Content |
|---|---|---|
| ENGINEERING_BEST_PRACTICES.md | 87KB | Runtime guards, LOG investigation, SCM jobs, build-vs-hire |
| BRANCHING_STRATEGY.md | 92KB | INV-000–009, INV-OH-001–008, branch naming, merge protocols |
| DOCUMENTATION_STANDARDS.md | 40KB | Frontmatter, headings, RFC 2119, SPDLC taxonomy |
| AGENT_WORKFLOWS.md | 21KB | Slash commands, multi-PR coordination, FP wave protocol |
| PLAN_SLC.md | 36KB | 7-phase plan, kill-switch framework, scope tiers |
| ARCH.md | — | Universal laws, quality attributes, SLOs, phase constraints |
| BLUE-001 | — | Mobile blueprint: Flutter, Riverpod, GoRouter, audio |
| BLUE-002 | — | Cloud blueprint: FastAPI, Cloud Run, GCS Signed URLs |
| BLUE-003 | — | Analytics + Operational: PostHog, BigQuery, CloudEvents |
| DR-020–024 | — | EventConstants, recording gate, shared mocks, Prefect, GitHub Pro |
