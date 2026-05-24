# Retrospective: Prompt-Level Inheritance Gap in Workspace Mode

## The Correction
The Operator identified a critical design flaw in the prompt-level inheritance mechanism for Workspace Mode:
* **The Gap**: When the Agent CLI (`agy`) boots, it loads the parent `GEMINI.md`. If the parent prompt lacks an explicit instruction to read and merge the child `GEMINI.md` file (if it exists in `SPAO_WORKSPACE_DIR`), the Agent will reload with only the parent ruleset on subsequent steps, completely ignoring local child overrides and extensions.
* **The Resolution**: Updated the parent `GEMINI.md` (Subsection 1.1) to include a strict instruction mandating that the Agent must locate, read, and merge the child `GEMINI.md` from the workspace root directory whenever `SPAO_WORKSPACE_DIR` is set.

## Codified Insight
1. **Dynamic Prompt Merging Invariant**: In a dual-context redirection model, the parent system prompt must explicitly command the Agent to load and merge the child's local prompt file (`GEMINI.md`) to prevent context drift and ensure local overrides remain active across agent reload cycles.
