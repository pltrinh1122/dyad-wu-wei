# WHAT-0079: The Ziran Flow Riverbed Framework

## 1. Intent & Purpose
This primitive codifies the exact physics of **Ziran Flow** within the Dao Engine. Following the epiphany of Ziran Navigation (`WHY-0070`) and the realization of the Passive Ziran Auditor (`WHAT-0077`), we require a formal ontological framework to handle exception events without sacrificing execution velocity or violating system safety.

The native architectural analogy for the system is **The Geological Riverbed**.

## 2. The Geological Riverbed Analogy
To eliminate the "Old-Dao" assumption that we are building a rigid, unyielding pipeline, we model execution as water carving a canyon.
*   **The Bedrock**: The absolute physical invariants (SPAO loop, `WIP-N=1`, Hard Gates). These do not change and form the absolute bounds of the system.
*   **The Soil Banks**: The `kb/` rules, specifications, and ontological schemas. These constrain the water, but are mutable.
*   **The Flow**: The Agent's semantic execution moving through the terrain.
*   **The Ziran Mechanic**: When the water hits the soil with *Turbulence*, it erodes the bank (the Passive Ziran Auditor demoting a bad rule). When the water runs *Laminar*, it deepens the channel (the Auditor promoting a rule). The boundary and the flow co-evolve.

## 3. The Dual-Phase Navigation Framework (Triage)
Because we operate in a deterministic physical substrate, Ziran Flow cannot be blind momentum. Exceptions must be strictly triaged into two categories to prevent catastrophic entropy.

### Phase 1: Gateway Triage
When an exception occurs during the SPAO loop, the system must immediately answer: *Is this Friction or Rupture?*
*   **Structural Rupture (Bedrock Rupture)**: Does this exception compromise the SPAO engine wrappers (`bin/node`), corrupt the state ledgers (`frontier_state.md`), risk remote environment damage, or fundamentally block the parent Path's objective?
*   **Turbulence (Friction)**: Is this a localized logic error, a failing offline test (`bin/run-tests`), or a semantic drift that is isolated to the current Node's container?

### Phase 2A: Handling Structural Rupture
If the triage identifies a Structural Rupture, Ziran Flow is suspended.
*   **Action**: Trigger an immediate, static Hard Gate (`sys.exit(1)`). Halt the primary sequence completely.
*   **Rule**: Do NOT push the state machine forward. Do NOT spin the exception off into the backlog. The current Path is entirely blocked until the engine or structural dependency is manually or orthogonally repaired.

### Phase 2B: Handling Turbulence
If the triage identifies the exception as mere Turbulence, the pure Ziran principles apply perfectly:
*   **Action (Trivial Turbulence)**: Remediate the issue inline using offline test containment (`./bin/run-tests`). 
*   **Action (Complex but Non-Blocking)**: If the fix requires deep work but *does not* block the parent Path's primary intent, isolate it into a new orthogonal Activity in the backlog. Revert the active branch to a known-laminar state and continue the primary sequence.
*   **Rule**: Treat the friction as passive telemetry. Push the SPAO state machine forward without over-analyzing the noise.
