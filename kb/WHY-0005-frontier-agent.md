# WHY-0005: Separation of the Frontier Agent from Functional Logic

## The Problem
When a single agent persona attempts to both write functional code (e.g., `agent-sg1`) and govern the rules of how the repository is managed, the system suffers from **contextual collapse**. The agent begins to optimize the global rules for its immediate local coding task, degrading the structural integrity of the SPAO loop. Furthermore, if the loop definition is tightly coupled to the specific model (e.g., Gemini), the orchestration cannot be ported to other LLM implementations.

## The Architectural Decision
We establish a dedicated **Frontier Agent** persona, entirely segregated from functional domain tasks.

1. **Why Frontier Agent instead of a model-specific name?**
   The designation Frontier Agent reflects a deliberate abstraction. By removing the model identity (e.g., `dz-cil`) from the persona name, we enforce the **Portability Axiom**. The rules and logic authored by the Frontier Agent can be dropped into an `agent-claude` repository, ensuring that our SPAO architecture remains universally applicable across different foundational models.

2. **Why decouple loop management from functional coding?**
   Separation of concerns. The Frontier Agent persona acts as the legislative branch of the repository, setting the invariants and loop constraints. The functional agents (e.g., `agent-sg1`, `agent-ziran`) act as the executive branch, executing code within those bounds. This prevents localized tasks from corrupting the global orchestration policy.
