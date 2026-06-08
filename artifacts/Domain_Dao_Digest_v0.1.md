# Domain Dao Digest v0.1: Family Legacy (familyloom.app)

## Abstract
This digest synthesizes the Tier 1-3 governance corpus of the Family Legacy (familyloom.app) project into a unified set of codified rules with addressable IDs. It serves as the foundational substrate for Domain Dao onboarding, ensuring operational autonomy respects the established boundaries of the project.

## 1. Architectural Laws (FL-ARCH-*)

### FL-ARCH-001: Law of Immutable Audit
- **Rule:** No state change to user-owned data shall occur without a cryptographically signed audit entry. All `MOD-` models MUST include an `audit_trail` object. Systems MUST reject any write operation that lacks a valid signature or lineage.

### FL-ARCH-002: Law of Local Primacy (Offline-First)
- **Rule:** The User Mission (`FEAT-`) MUST be executable regardless of the Network State. All `FEAT-` logic MUST hire a `MOD-` layer that supports optimistic local writes. Lack of connectivity MUST NOT block critical missions. Mobile environments MUST implement sync queues; Cloud environments MUST implement idempotency.

### FL-ARCH-003: Session Continuity Invariant
- **Rule:** A recording session MUST be fully recoverable after process termination or device restart. Zero data loss is required; session state is treated as append-only.

### FL-ARCH-004: Law of Least Privilege Identity
- **Rule:** Access to a resource is denied by default and granted only via a scoped, short-lived token. Every `INFRA-` service MUST validate a token before executing a `MOD-` operation. Identity MUST NOT be inferred; it MUST be explicitly proven.

### FL-ARCH-005: Law of Data Sovereignty
- **Rule:** User data is the user's alone. All `MOD-` storage MUST be siloed per-user. No cross-user queries or aggregate indexing.

### FL-ARCH-006: Component Paradigms
- **Rule:** All `FEAT-` logic MUST use NotifierProvider/ConsumerWidget patterns. All `MOD-` models MUST use Freezed. All `MOD-` schemas MUST be defined as Drift tables. All `INFRA-` networking MUST use Dio. Media uploads MUST use GCS Signed URLs; API containers MUST NEVER directly stream media.

## 2. Invariants & Branching Strategy (FL-INV-*)

### FL-INV-001: Authorized Integrations
- **Rule:** Every authorized Pull Request MUST serve a previously documented Change Request. All commits on `main` and Support-Branches MUST exist exclusively as the result of an approved Pull Request merge.

### FL-INV-002: Lineage Integrity
- **Rule:** Every hotfix commit present in a legacy Support-Branch MUST also be present in the `main` branch before its associated Change Request ticket is closed.

### FL-INV-003: API & Schema Contract
- **Rule:** The current database schema and API endpoints MUST remain fully backward compatible with the contract requirements of at least the N-1 active Support-Branch.

### FL-INV-004: Atomic Scoping
- **Rule:** A single Pull Request MUST encapsulate changes belonging to only one release lifecycle (i.e., exclusively Cloud changes OR exclusively Mobile changes).

### FL-INV-005: Environment Branch Prohibition
- **Rule:** The repository MUST NOT contain long-lived environment branches (e.g., `qa`, `staging`, `prod`).

### FL-INV-006: Content Parity Protocol
- **Rule:** Every Support-Branch and `main` MUST keep its working state byte-identical to the deployed source-of-truth branch on the deployed-content file set.

### FL-INV-007: Governance Parity Protocol
- **Rule:** Every active forward branch MUST keep its working state byte-identical to `main` on the governance-paths set.

### FL-INV-008: Append-Only Ledger
- **Rule:** Every state change on a ref pushed to origin MUST be append-only. Force pushes and mutable history rewrites on shared/origin branches are strictly prohibited.

## 3. Operational Hygiene (FL-AP-*)

### FL-AP-001: Worktree Strictness
- **Rule:** Every entry in `git worktree list` MUST have a worktree path whose tail is byte-identical to the branch ref it tracks.

### FL-AP-002: Ephemeral Branch GC
- **Rule:** When a `solo/*` or `shared/*` branch's PR is merged or closed, its local ref MUST be deleted, and any worktree associated with it MUST be removed in the same working session. This cleanup MUST execute as one logical atomic operation.

### FL-AP-003: Sync State Push
- **Rule:** Every commit on a `solo/*`, `shared/*`, or `tba/*` branch MUST be pushed to its tracking remote before the workstation goes idle.

### FL-AP-004: Branch Nomenclature
- **Rule:** Every branch ref pushed to `origin` MUST match recognized canonical formats (`solo/<anchor>/<alias>/<slug>`, `shared/<anchor>/<slug>`, etc.).

## 4. Engineering Conventions (FL-CONV-*)

### FL-CONV-001: Invariant-Driven Troubleshooting
- **Rule:** Differentiate runtime guards (production boundary inputs), debug asserts (internal contracts), and test-time discoveries (test expectations). Do not leave boundaries undefended in release builds.

### FL-CONV-002: Observability Tracing
- **Rule:** Route production diagnostics through the existing observability surface (PostHog). Analytics events MUST NOT contain PII. Always use constants from `event_constants.dart` over string literals.

### FL-CONV-003: LOG-Driven Anomaly Resolution
- **Rule:** Use a structured LOG artifact (following M.4 cadence: hypothesis, raw outcome, interpretation) for complex troubleshooting before deploying fixes. Maintain strict separation of raw observation from interpretation.

### FL-CONV-004: Test-First Discipline
- **Rule:** Implement strict RED -> GREEN. Tests MUST assert observable behavior, not implementation surfaces. Distinguish true RED tests from regression coverage.

## 5. Toolchain Practices (FL-TOOL-*)

### FL-TOOL-001: Shared Mocks
- **Rule:** Integration tests SHOULD use shared mocks from `test/utils/test_helpers.dart` rather than declaring local ones to prevent drift.

### FL-TOOL-002: CI Enforcement
- **Rule:** All governance validations (Content Parity, Governance Parity, Path validations) are backed by automated CI linters. CI failures block merge.

### FL-TOOL-003: Build-Mode Selection
- **Rule:** Investigation phases SHOULD use debug builds (`flutter run --debug`) over release builds. However, at least one release-build re-verification phase MUST occur before closing an investigation.
