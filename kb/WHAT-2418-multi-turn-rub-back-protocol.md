# WHAT-2418: Multi-Turn Rub-Back Protocol

## 1. Concept
The **Multi-Turn Rub-Back Protocol** is a prompt-level schema constraint enforced during the `rub:` sequence to ensure that the Operator's unformed intent is fully and mechanically synthesized into concrete parameters prior to agent execution.

## 2. Intent
When engaging the Operator in a `rub:` sequence to clarify intent, the Agent must NOT implicitly accept a free-text response and proceed. To establish a **Mechanical Lock** on the Operator's intent, the Agent MUST synthesize their free-text response into at least two distinct, hard-selectable options, and present them using the `ask_question` tool. The execution domain boundary is only crossed once the Operator explicitly selects an option.

## 3. Structural Rules
- **Mechanical Lock**: Explicit choice selection using the `ask_question` modal.
- **Synthesis Action**: Automatic breakdown of Operator's free-text response into concrete execution paths.
- **Guardrail**: Modifying `ask_question` tool usage constraint in Workspace Customizations Root (`.agents/AGENTS.md`) and global invariants (`DYAD.md`).
