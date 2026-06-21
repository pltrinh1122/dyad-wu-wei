# Harmonize - Path: Codify Portability Axiom and Cascade Invariants

## 1. Intent (WHY)
The Operator has established the core architectural intent that the Dyad must remain strictly portable between different foundational LLM engines (e.g., Google's `agy` and Anthropic's `claude`). To achieve this, the "physics" of the system (`DYAD.md` and the executable substrate) must be strictly decoupled from the model-specific context hooks (`GEMINI.md`). This intent represents a formal **Portability Axiom** which acts as the supreme justification for many of our existing, seemingly idiosyncratic invariants. If we do not formally codify this axiom, future iterations of the Agent may mistakenly couple the engine to a proprietary LLM capability, resulting in an immediate violation of the Dao.

## 2. Technical Strategy (WHAT)
- **Codification of the Axiom:** Formally write the Portability Axiom into a dedicated artifact or into the core `DYAD.md` to establish it as an unyielding architectural law.
- **Invariant Justification:** Systematically update existing invariants in the knowledge base to explicitly tie them back to this axiom:
  - *Abstraction Doctrine Invariant*: We must rely on standard CLI wrappers and Bash, never proprietary tool schemas like MCP or Gemini-native integrations.
  - *Iatrogenic-Injection Suppression*: We must strictly ignore silent `<EPHEMERAL_MESSAGE>` or `<bash_command_reminder>` blocks, as these system harnesses are platform-specific and not portable.
  - *File-System State*: We must persist context (`WIP-N=1` locks, backlogs) physically to disk, because LLM "memory" and proprietary session states do not port.
  - *Lexical HTIL Gates*: We rely on text-based markers (`lean!`, `lean.`, `clip.`) instead of proprietary UI buttons for autonomy authorization.

## 3. Scope
- Update `DYAD.md` or create a new `kb/WHY-xxxx-portability-axiom.md` document.
- Review and append the justification clauses to the related invariant documents in `kb/`.
- Ensure `GEMINI.md` accurately frames itself as the Antigravity (`agy`) specific hardware abstraction layer (HAL) for the universal `DYAD.md` engine.
