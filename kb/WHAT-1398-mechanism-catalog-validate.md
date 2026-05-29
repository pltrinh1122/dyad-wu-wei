# WHAT-1398: Mechanism Catalog - Validate Family

## Concept
The Dyad Practice dictates that the `Validate` family of mechanisms acts to anchor generated hypotheses back to empirical reality. A core tenant is that validation is structurally distinct from generation to avoid "marking our own homework."

## Mechanisms
1. **Falsification (Dialectical Falsification)**: Already codified in `WHY-0091`. The act of proposing a thesis and ruthlessly attempting to break it with empirical evidence.
2. **Triangulation**: A new mechanism introduced from the Dyad Practice. Triangulation involves seeking a third, independent vector to verify a binary assertion. If the Agent and the Operator agree, but lack an independent anchor (e.g., a test suite, an external document, an error log), the agreement is considered insufficient.
3. **Grounding**: The enforcement of tying abstract concepts to literal, executable lines of code or exact filesystem paths.

## Structural Requirements
- Any Node output that introduces new concepts MUST explicitly reference its validation mechanism.
- Triangulation MUST be employed when resolving architectural disputes.
