# WHAT-1304: Harmonize Recovery Protocol with Wu-wei NBA Handoff Protocol Specification

## Specification
The Frontier Recovery Protocol (HOW-1170) must be physically decoupled from interactive and conversational communication logic:

1. **Orthogonality of State-Assertion**:
   HOW-1170 must exclusively focus on physical state and environmental validation (checking git-status, status commands, ROM currency, running offline tests).
   
2. **Interaction Handoff**:
   Once the physical verification steps of the recovery protocol pass, control and interaction policy must be delegated to the universal Wu-wei NBA Handoff Protocol (WHAT-1043).
   
3. **No Interactive Logic**:
   The diagnostic script/documentation of HOW-1170 must not define custom chat patterns or handoff dialogs.

## Implementation Details
HOW-1170 Section 3 is updated to reference WHAT-1043 for all post-recovery interactions.
