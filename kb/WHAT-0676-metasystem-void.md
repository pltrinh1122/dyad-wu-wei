# WHAT-0676: The Void of the Metasystem (Agnostic Payload Execution)

## 1. Context and Origin
This document codifies the alignment contract established in Node 677 regarding the boundaries and responsibilities of the Metasystem (the `agent-meta` tier and the SPAO execution loops).

## 2. The Core Principle
The Metasystem operates strictly within "The Void." It is an architectural conveyor belt that moves work through the `SPAOR` sequence (`status -> plan -> checkout -> act -> reflect`), but it must remain **completely agnostic** to the payload it is processing.

## 3. Strict Decoupling Invariants
- **No Contextual Routing**: The agentic governance loop MUST NOT fork its state machine logic based on the content of the payload. Whether a node is refactoring Python code, adding CSS, or updating a knowledge base document, the SPAO execution loop executes identically.
- **Payload Ignorance**: The engine must never inspect the payload to alter invariants or validation gates. For instance, the system cannot decide to bypass tests simply because the payload contains only documentation.
- **Architectural Purity**: If `agent-meta` becomes aware of functional domain rules, it collapses the intended boundaries and causes catastrophic context bloat. Intelligence and domain constraints belong entirely to the payload (the issue descriptions, prompts, and functional `agent-dao` or `agent-platform` boundaries).

## 4. Enforcement
Any modification to the `kernel/` or `bin/` execution scripts that introduces conditional logic checking the nature of the work being performed (e.g., checking file extensions to skip CI steps) is an explicit violation of this protocol and must be falsified during review.
