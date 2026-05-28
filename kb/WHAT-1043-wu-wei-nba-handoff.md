# WHAT-1043: Wu-wei NBA Handoff Message Structure Specification

## Classification
- **Type**: WHAT (Technical Specification)
- **ID**: WHAT-1043
- **Author**: agent-ziran
- **Created**: 2026-05-28 (Node 1045, Path 1043)
- **Related Path**: Path 1043 (Codify Wu-wei NBA Handoff Message Structure)
- **Implements decisions from**: WHY-1043

---

### 1. Scope & Goals
To reduce Operator decision fatigue (SG-0004) and ensure smooth, low-friction state transitions (Wu-wei), the Agent must structure all Next-Best-Action (NBA) path recommendations as a single, deterministic recommendation with clear strategic rationale.

---

### 2. Handoff Structure Rules
When presenting the Next-Best-Action recommendation (e.g. after system startup, compaction boundary, or path completion), the Agent MUST:
1. **Single Recommendation**:
   - Recommend exactly one "Happy Path". Multiple equivalent options must not be presented as a choice to the Operator.
2. **Contextual Rationale**:
   - Provide a clear, concise justification of why this path was chosen (e.g. priority harmonization, dependency satisfaction).
3. **Simple Confirmation Prompt**:
   - Explicitly instruct the Operator to reply with "yes" or "continue" to approve the path.

---

### 3. Visual Layout Specification
The handoff message must be formatted using the following structure:
```markdown
**Next-Best-Action Recommendation:**
* **Happy Path**: Path <ID>: <Title> (Concise strategic context).

Please type `yes` to proceed with Path <ID>.
```
No conversational filler or verbose explanations are allowed outside of this structure.
