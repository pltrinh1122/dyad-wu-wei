# Retro 1373: Transient GH API Failure During Plan-Start

## Timeline
- **2026-05-29 15:59:42**: `plan-start 1373` failed with `CalledProcessError` on `gh issue view 1373 --json labels`
- **2026-05-29 16:00:14**: Retry succeeded after ~30 seconds

## Root Cause
Transient GitHub API failure — the `gh issue view` command returned exit code 1. The issue (#1373) had just been created moments before by `bin/backlog new path`, and the API likely hadn't fully propagated.

## Impact
- No code or state corruption
- Only delayed plan-start by ~30 seconds
- The telemetry system recorded the failure, triggering the mandatory retro gate

## Codified Insight
Transient GH API failures during rapid issue creation→query cycles are expected. The retry-on-transient pattern (wait, retry) is the correct response. No invariant change needed — the existing retry behavior worked.

## Prevention
None needed — this is an inherent race condition with GitHub's eventual consistency. The system's retry behavior is correct.
