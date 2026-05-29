# External Project Support Protocol

> **Status**: DRAFT
> **Node**: 1329 | **Path**: 1323

## 1. Purpose

This protocol defines the bilateral communication channel between the DZ-CIL engine and external project workstations. It enables an Agent operating on a separate workstation — with a read-only DZ-CIL clone as its Dao reference — to request remedies, report amendments, escalate blockers, and feed learnings back to the engine.

## 2. Operating Model

```
┌─────────────────────┐         ┌──────────────────────┐
│  External Project   │         │     DZ-CIL Engine    │
│    Workstation      │         │                      │
│                     │         │                      │
│  [Project Repo]     │  SUPPORT│  [DZ-CIL Repo]       │
│  - Domain Dao       │  TICKET │  - Generic Protocol   │
│    Digest (private) │ ──────> │  - Issue Template     │
│  - Source code      │         │  - kb/ primitives     │
│  - Tests            │         │                      │
│                     │ <────── │                      │
│  [Read-Only Clone]  │ REMEDY  │  [Operator Review]   │
│  - DZ-CIL kb/       │         │                      │
│  - Protocol docs    │         │                      │
└─────────────────────┘         └──────────────────────┘
```

### Key Principle: IP Isolation

The DZ-CIL engine (this repository) contains ONLY the generic protocol mechanics. All domain-specific content — governance rules, architecture constraints, business decisions, project identifiers — resides exclusively in the external project's private repository. The engine never caches or stores domain-specific content.

## 3. Ticket Types

### 3.1 Amendment

**When**: The Agent discovers a gap, error, or missing rule in the project's Domain Dao Digest during active work.

**Flow**:
1. Agent files `[SUPPORT]` issue with type "Amendment"
2. Issue describes the gap, its impact, and a proposed rule change
3. Operator reviews and ratifies (or rejects with guidance)
4. Agent updates the Domain Dao Digest in the project's private repo
5. Support issue closed with reference to the project-side commit

**SLA**: Non-blocking amendments batched per session. Blocking amendments require Operator response before Agent can proceed.

### 3.2 Escalation

**When**: The Agent encounters a blocking ambiguity that requires Operator domain knowledge to resolve. The Agent cannot infer the correct action from the existing digest or project documentation.

**Flow**:
1. Agent files `[SUPPORT]` issue with type "Escalation" and blocking flag = Yes
2. Agent halts the affected work package (continues on non-dependent work if available)
3. Operator provides guidance via issue comment
4. Agent resumes work, applying the guidance
5. If the guidance reveals a digest gap, a follow-up Amendment ticket is filed

**SLA**: Blocking escalations should receive Operator response within the current work session.

### 3.3 Tooling

**When**: The Agent identifies a need for a new DZ-CIL skill, wrapper, or infrastructure component that would benefit all external projects (not just the requesting one).

**Flow**:
1. Agent files `[SUPPORT]` issue with type "Tooling"
2. Issue describes the capability gap and proposed solution
3. Operator evaluates whether the tool is generic enough for DZ-CIL
4. If accepted: DZ-CIL creates a backlog Path for the tool
5. If rejected: Agent works around the gap using project-local tooling

**SLA**: Non-blocking. Tooling requests are queued for the next DZ-CIL planning cycle.

### 3.4 Retrospective

**When**: A work session on the external project produces learnings that should flow back to the DZ-CIL engine's knowledge base — new anti-patterns, process improvements, or corrections to meta-process rules.

**Flow**:
1. Agent files `[SUPPORT]` issue with type "Retrospective"
2. Issue contains the structured retro (What happened, Root cause, Codified insight)
3. Operator reviews whether the insight is generic (applicable to all projects) or project-specific
4. Generic insights: codified as DZ-CIL `kb/WHY-*` or GEMINI.md rule updates
5. Project-specific insights: Agent updates the project's Domain Dao Digest

**SLA**: Non-blocking. Retros batched and reviewed during DZ-CIL planning cycles.

### 3.5 Bug

**When**: The Agent encounters a defect in DZ-CIL's toolchain, scripts, or orchestration logic during external project work.

**Flow**:
1. Agent files `[SUPPORT]` issue with type "Bug"
2. Issue includes reproduction steps, expected vs actual behavior, and environment details
3. Operator triages and routes to DZ-CIL's standard bug resolution pipeline
4. Fix delivered via DZ-CIL's governed SPAOR loop

**SLA**: Blocking bugs escalated immediately. Non-blocking bugs queued normally.

## 4. Domain Dao Digest Architecture

Each external project maintains its own Domain Dao Digest — a curated, addressable rule set governing the Agent's behavior on that project.

### 4.1 Digest Location

| Component | Location | Visibility |
|-----------|----------|------------|
| Digest (source of truth) | External project repo | Private |
| Protocol docs | DZ-CIL `kb/` | Repo-scoped |
| Issue template | DZ-CIL `github_templates/` | Repo-scoped |

### 4.2 Digest Format

Digests follow a sectioned monolith format with addressable IDs:
- `INV-NNN` — Invariants (MUST rules)
- `CONV-NNN` — Conventions (SHOULD rules)
- `AP-NNN` — Anti-Patterns (MUST NOT rules)
- `TOOL-NNN` — Toolchain constraints
- `ARCH-NNN` — Architecture constraints

ID prefixes are project-scoped (e.g., a project may use `FL-INV-*` or `ACME-INV-*`). DZ-CIL does not dictate prefixes.

### 4.3 Digest Loading

When the Agent begins work on an external project:
1. Load the project's Domain Dao Digest from the project's repo
2. Treat all rules as operational constraints for the session duration
3. Any corrections discovered → batch for Amendment support ticket

### 4.4 Amendment Lifecycle

```
Agent discovers gap
  → Files [SUPPORT] Amendment ticket (on DZ-CIL)
  → Operator ratifies or rejects (via issue comment)
  → Agent updates Digest in project repo (via project PR)
  → Support issue closed with project commit reference
```

## 5. Workstation Provisioning Checklist

When setting up a new external project workstation:

- [ ] Project repo cloned with write access
- [ ] Read-only DZ-CIL clone available for protocol reference
- [ ] Project's Domain Dao Digest exists in the project repo
- [ ] Agent can file issues on DZ-CIL repo (for support tickets)
- [ ] Project-specific toolchain installed and verified
- [ ] First work package assigned by Operator

## 6. Guardrails

1. **IP Isolation**: DZ-CIL MUST NOT contain any project-specific rules, identifiers, architecture decisions, or business constraints. All domain content stays in the project's private repo.
2. **Generic Protocol**: The support template and this protocol document are project-agnostic. They serve any external project, not a specific one.
3. **Operator Gate**: All amendments, escalations, and tooling requests flow through the Operator. The Agent cannot self-approve changes to the engine.
4. **Traceability**: Every support ticket includes a session ID for audit trail. Every amendment links back to its support ticket.
