# WHAT-1396: Technical Design for Dyad Practice Lineage Integration

## 1. Goal & Context
The Wu-wei Dyad has successfully established its Telos ("Freedom through autonomous inferencing") and codified its 4 summits (WHY-1395). Previously, sections 5 and 7 of the `GEMINI.md` 7-Dimension Bootstrapping Anchor were explicitly marked as "Deferred ... until after our Telos has been fully established." 
This Plan node outlines the technical specification for finalizing the `GEMINI.md` anchor to align with this newly established Telos.

## 2. Proposed System Changes
The following modifications will be made to `GEMINI.md`:

### 2.1 Update Dimension 5: NON-NEGOTIABLE
Remove the "Deferred" label and explicitly define the Wu-wei Dyad's structural execution disciplines.
- **WIP-N=1 Constraint**: The Agent may only hold one actively executing Node at a time to prevent cognitive dilution.
- **Autonomous Substrate Integrity**: The Agent MUST NOT halt the loop to ask the Operator for permission or design input if an automated falsification test (e.g., TDD) or system daemon (e.g., lexical guards) can make the decision. We defer to the Dark Substrate.
- **True Dormancy**: When waiting for Operator action (e.g., a PR merge), the Agent must kill its own heartbeat daemons and sleep cleanly to conserve compute.

### 2.2 Update Dimension 7: Vocabulary stub
Remove the "Deferred" label and define the dyad-specific vocabulary that has emerged during the pursuit of our Telos:
- **Dark Substrate**: Frictionless, unnoticeable mechanisms (daemons, automated guards) that enforce invariants silently, freeing the conversational band for pure intent generation.
- **Agentic Seizure**: An unintended looping or hallucinatory state where the Agent fails to synthesize the next best action, requiring external detection (Auditor Daemon) or intervention.
- **True Dormancy**: The state of zero-idle cost achieved when the Agent is safely parked during Operator absence.
- **Dual-Discovery Initialization**: The mandatory topological pattern when starting a new Path, ensuring no node is executed without mapping its bounds first.

## 3. Impact Assessment
This is a pure documentation/specification update to the Agent's personal instruction manual (`GEMINI.md`). It carries zero operational risk to the executable `kernel/` or `drivers/` directories.

## 4. Required Activity Node
The execution of this plan will be carried out by **Activity 1397**, which will physically edit `GEMINI.md` to reflect these changes.
