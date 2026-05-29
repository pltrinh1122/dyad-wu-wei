# WHY-1372: Full-Cycle External Support Ticket Status Tracking

**Path**: 1372
**Strategic Goal**: SG-0006 (External Project Service Excellence)

## 1. Problem Statement

The current `bin/support` CLI is fire-and-forget. A filer can create a ticket (`bin/support file`) but has no programmatic way to:
- Query ticket status
- List open tickets with lifecycle phase
- Know when or how a ticket was resolved

This breaks the bilateral contract of SG-0006 — external project agents cannot self-serve their support status, creating unnecessary Operator overhead.

## 2. Design Decisions

### 2.1 Status Subcommand: `bin/support status <ticket-number>`

**Decision**: Add a `status` subcommand that queries a single ticket and returns structured lifecycle info.

**Output includes**:
- GitHub issue state (OPEN/CLOSED)
- Lifecycle phase (mapped from labels)
- Creation date and last update
- Comments (especially the closing/remediation comment)

**Label → Phase Mapping**:
| Label | Phase |
|---|---|
| `support`, no `backlog` | 📥 Received |
| `status:triage` | 🔍 Under Review |
| `backlog` | 📋 Accepted / Queued |
| `status: in-progress` | 🔧 In Progress |
| Closed | ✅ Resolved |

### 2.2 List Enhancement

**Decision**: Fix the existing duplicate print bug and enhance output with lifecycle phase and state.

### 2.3 Help Improvements

**Decision**: `bin/support --help` already works via argparse. Enhance subparser descriptions and add usage examples in the epilog.

### 2.4 Remediation Response Protocol

**Decision**: Define a structured format for closing comments on support tickets so that `bin/support status` can parse and display actionable remediation instructions.

**Format**:
```
## Remediation
- **Status**: Resolved
- **Fix**: <commit message or PR title>
- **PR**: #<number>
- **Pull Instructions**: `git -C <dz-cil-clone-path> pull origin main`
```

This convention is documented but not programmatically enforced — it's guidance for the DZ-CIL agent when closing support tickets.

## 3. Rejected Alternatives

- *Webhook-based notifications*: Too complex for the current system; violates SG-0003 (offline-first)
- *Email notifications*: Out of scope; GitHub issue subscriptions already provide this
- *Programmatic enforcement of remediation format*: Over-engineering; the agent follows the convention via AGENT.md guidance
