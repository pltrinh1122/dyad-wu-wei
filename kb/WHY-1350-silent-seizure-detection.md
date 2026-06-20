# WHY-1350: Silent Seizure Detection via Audit Daemon Liveness Rule

**Source**: Intake #1233 (Healer)
**Path**: 1350
**Strategic Goals**: SG-0002 (Gateless Autonomous Execution), SG-0003 (Preservation of Autonomous Velocity)

## 1. Problem Statement

The system cannot self-detect **silent seizures** — cognitive-loop freezes where:
- Telemetry/transcript stops advancing
- No failing tests are produced
- The existing `seizure_detection` rule (rising `test-fail-*.json` count) never fires
- The `stale_active_node` rule checks state consistency, not liveness

Both historical Healer cases were silent freezes detected **only by the human Operator**. This violates SG-0002 (the Operator must remain a manual gatekeeper for freeze detection) and SG-0003 (undetected freezes are total throughput collapse).

## 2. Design Decisions

### 2.1 Liveness Signal: `frontier_state.yml` Modification Timestamp

**Decision**: Use the filesystem modification time (`mtime`) of `artifacts/frontier_state.yml` as the monotonic progress marker.

**Rationale**:
- Every SPAOR phase transition mutates the frontier state (plan-start, plan-finish, checkout, reflect)
- The `frontier_state.yml.sha256` checksum file is updated alongside it
- No additional instrumentation needed — the signal already exists
- Granularity matches the SPAOR loop cadence

**Rejected alternatives**:
- *Telemetry write timestamp*: Requires new instrumentation; telemetry may not exist in all modes
- *Active-node phase transition*: Requires parsing frontier state content, not just checking mtime
- *Git commit timestamp*: Too coarse (commits happen at end of Act phase, not during)

### 2.2 Rule Type: New `liveness_stall` Rule

**Decision**: Create a new rule type `liveness_stall` in the audit daemon registry, rather than extending `stale_active_node`.

**Rationale**:
- `stale_active_node` checks **state consistency** (active pointer vs completed status)
- Liveness is a fundamentally different concern — **time-since-progress**
- Separate rule type allows independent configuration (threshold, alert level)
- Clean separation of concerns in the RULE_REGISTRY

### 2.3 False-Positive Guard: Active Node Required + Minimum Threshold

**Decision**: The liveness rule fires ONLY when:
1. An active node exists in the frontier (i.e., the system is expected to be working)
2. The `frontier_state.yml` mtime has not advanced for longer than the configured `stall_threshold_minutes`

**Legitimate idle states that do NOT trigger**:
- Active node is `None` (system is idle between SPAOR cycles)
- System is in HITL gate (PR awaiting review) — the active node is set to `None` after reflect
- Clean halt / session end

**Design rationale**: The Healer's key insight — distinguish "expected to be progressing but isn't" from "legitimately idle." An active node pointer is the definitive signal that work is expected.

### 2.4 Stall Threshold: 15 Minutes (3 Daemon Ticks)

**Decision**: Default `stall_threshold_minutes: 15`

**Rationale**:
- Daemon ticks every 5 minutes (`timer_interval: 5m`)
- 15 minutes = 3 consecutive ticks with no frontier progress
- Short enough to catch real freezes within a reasonable window
- Long enough to avoid false positives during legitimate long-running operations (e.g., large test suites, complex file edits)

### 2.5 Daemon Activation: Already Solved

**Decision**: No additional work needed.

**Rationale**: The Healer noted the daemon had no cron entry at time of intake. This is now solved — the Agent establishes a `*/5 * * * *` cron via the `schedule` tool during the Bring-Up Process (DYAD.md §2.5). Verified operational (current session tick count: 30+).

## 3. Implementation Plan

1. Add `evaluate_liveness_stall` function to `drivers/audit_daemon.py`:
   - Check `frontier_state.yml` mtime
   - Compare against current time
   - Fire if delta exceeds threshold AND active node exists
2. Register `liveness_stall` in `RULE_REGISTRY`
3. Add rule configuration to `infra/audit-daemon/audit_config.yml`
4. Add tests to `tests/test_audit_daemon.py`

## 4. Falsifiable Success Criteria (from Healer)

- **Positive**: Frontier mtime frozen + active node exists + 15 min elapsed → detector emits STALL alert
- **Negative control**: No active node (clean idle) + frontier mtime frozen → does NOT fire
