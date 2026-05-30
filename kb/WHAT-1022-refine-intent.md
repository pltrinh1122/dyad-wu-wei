# WHAT-1022: Refine Wu-wei Dyad Intent Understanding Specification

## Classification
- **Type**: WHAT (Technical Specification)
- **ID**: WHAT-1022
- **Author**: agent-ziran
- **Created**: 2026-05-28 (Node 1024, Path 1022)
- **Related Path**: Path 1022 (Refine Wu-wei Dyad Intent Understanding)
- **Implements decisions from**: WHY-1022

---

### 1. Scope & Goals
To guarantee system harmonization and prevent execution drift without introducing conversational fatigue (SG-0004), the Agent's intent understanding must parse Operator instructions through context-anchored verification rules.

---

### 2. Intent Parsing Rules
When the Operator submits a chat request, the Agent MUST resolve the intent using the following hierarchy:
1. **Backlog & Active Path Verification**:
   - Check if the instruction refers to an open or prioritized path in the backlog.
   - If yes, prioritize actions mapping to that path's pending nodes.
2. **Persona Assignment Check**:
   - Resolve the required executing persona (`SPAO_PERSONA_ID`) from `WHAT-0062` or `WHAT-0065` for the target path.
   - The Agent must execute the task using that correct persona.
3. **Execution Command Mapping**:
   - Direct command requests must be mapped to whitelisted adapter CLI commands (e.g. `bin/node`, `bin/prompt`, `bin/rt`). Raw shell commands are forbidden.

---

### 3. Bilateral Chat Integration
- All interpreted intents must be acknowledged using the strict protocol format:
  `Hai. (Intent: <Parsed Intent Summary>. Status: <Subsequent Action>.)`
- Any ambiguous intent that cannot be resolved through the backlog context must trigger the Chat Immediacy Clarification Protocol.
