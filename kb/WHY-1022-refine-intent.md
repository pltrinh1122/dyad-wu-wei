# WHY-1022: Refine DZ-CIL Intent Understanding

## Classification
- **Type**: WHY (Decision Record)
- **ID**: WHY-1022
- **Author**: agent-ziran
- **Created**: 2026-05-28 (Node 1023, Path 1022)
- **Status**: Accepted

---

## 1. Context

Under the Bilateral Chat Interaction Protocol (Rule 9), the response "Hai." is a strict execution contract guaranteeing immediate UI unblocking. When the Operator provides an intent via chat, the Agent must instantly interpret the intent, queue all necessary actions asynchronously to the backlog, and reply immediately.

However, a naive receipt of instructions can lead to misalignment if the Agent fails to interpret the Operator's intent through the lens of the overall DZ-CIL context, its active strategic goals, the current Dao, and Ziran (natural execution). 

To ensure semantic and operational coherence without manual clarification loops (which violate SG-0004), the Agent's intent understanding must be explicitly grounded in the active knowledge index, current active/prioritized paths, and specific workspace constraints.

---

## 2. Options Considered

### Option A: Static Mapping of Commands
* **Thesis**: Map specific keywords to deterministic commands.
* **Antithesis**: Brittle and violates Ziran. The Operator cannot communicate high-level intent naturally.
* **Result**: Rejected.

### Option B: Pure LLM Synthesis without Contextual Anchoring
* **Thesis**: Rely entirely on the LLM's default understanding of the Operator's prompt.
* **Antithesis**: Highly prone to hallucination or ignoring local rules (e.g., trying to run git directly instead of `./bin/git`, or forgetting persona restrictions).
* **Result**: Rejected.

### Option C: Context-Anchored Intent Resolution (DZ-CIL Intent Understanding) ✅ CHOSEN
* **Thesis**: The Agent dynamically infers the Operator's intent by aligning the chat input with the active backlog, prior retrospects, active strategic goals, and persona assignments.
* **Result**: Accepted. This achieves the optimal balance of immediate UI unblocking and correct execution.

---

## 3. The Decision

Adopt **Option C: Context-Anchored Intent Resolution**.
All Operator chat intents must be parsed by verifying:
1. Active Path Context: Check if the request matches or is a logical next-step for the active/prioritized paths.
2. Persona and Domain Boundaries: Verify which logical persona is registered to execute the inferred task.
3. System Command Abstractions: Map the actions to whitelisted adapter CLI commands (e.g. `bin/prompt`, `bin/node`) rather than raw bash executions.
