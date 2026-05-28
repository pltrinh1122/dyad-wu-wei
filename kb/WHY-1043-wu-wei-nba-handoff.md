# WHY-1043: Wu-wei NBA Handoff Message Structure

## Classification
- **Type**: WHY (Decision Record)
- **ID**: WHY-1043
- **Author**: agent-ziran
- **Created**: 2026-05-28 (Node 1045, Path 1043)
- **Status**: Accepted

---

## 1. Context

Under the Synergistic Human-Agent Partnership (NS-0001), after a context break (such as an agent restart, compaction boundary, or completing a path), the Operator must redirect the Agent. 

Previously, the Agent would present a generic list of next-best-actions or ask open-ended questions. This forces the Operator to re-analyze the active goals, dependencies, and scores, causing cognitive load and decision fatigue (violating SG-0004).

To align with the Wu-wei (minimum friction) and Ziran (natural action) principles, the Agent must formulate a single, optimal next best action (NBA) recommendation with clear strategic reasoning, allowing the Operator to simply approve it with a "yes" command.

---

## 2. Options Considered

### Option A: Flat List of Options
* **Thesis**: Absolute transparency. Let the Operator choose from all high-scoring paths.
* **Antithesis**: Low velocity. Operator has to manually parse and evaluate each option.
* **Result**: Rejected.

### Option B: Open-Ended Inquiry
* **Thesis**: Direct delegation. Let the Operator decide what to do next.
* **Antithesis**: Shifts the cognitive burden entirely to the human.
* **Result**: Rejected.

### Option C: Deterministic "Happy Path" Handoff ✅ CHOSEN
* **Thesis**: The Agent evaluates all paths, selects the highest-scoring candidate, presents the rationale, and asks for a simple "yes" approval.
* **Result**: Accepted. This preserves the Operator's Flow State and accelerates transitions.

---

## 3. The Decision

Adopt **Option C: Deterministic "Happy Path" Handoff**.
The Agent will present the recommendation using a structured and predictable visual layout:
1. **Strategic Context**: Concise reasoning explaining *why* this path is the highest priority.
2. **Actionable Prompt**: A single, clear action that the Operator can approve.
