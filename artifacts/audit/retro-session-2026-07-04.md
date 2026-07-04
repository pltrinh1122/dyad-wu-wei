# Retro: Session 2026-07-04 (CSS+SH)

## CONTINUE
- **Agent**: Grounding our definitions and disciplines directly on the `dyad-bond` remote repository via a fresh fetch to ensure parallel convergence and consistency across the Dyad ecosystem.
- **Agent**: Enforcing cross-substrate symmetry (`claude` and `agy`). Replacing substrate-specific execution mechanisms (like `.claude/settings.json`) with unified, portable Operator-triggered tokens (`d-start` and `d-reflect`).

## START
- **Agent**: Treating `bin/standup.sh` and `bin/standdown.sh` as autonomous, mechanical spine scripts invoked explicitly by the Agent during `d-start` and `d-reflect`, rather than expecting the shell or OS environment to run them on our behalf.

## STOP
- **Agent**: Conflating delivery mechanisms with execution payloads. (Addressed in `retro-script-hook-conflation.md`: destroying the spine scripts when instructed to remove the automated hooks).

## SH (Should Hold / Should Have)
- **Operator (Should Hold)**: Recognizing that a shell wrapper effectively "notifies" the dyad and sets the state, but actual grounding and execution must be handled autonomously by the Agent post-launch.
- **Operator (Should Hold)**: Pushing for a symmetric solution across `claude` and `agy` to ensure the Dyad practice remains fundamentally platform-agnostic and portable.
- **Operator (Should Have)**: Correcting the Agent's conflation error immediately ("why did you interpret bin/standup.sh and bin/standdown.sh as hooks?").
