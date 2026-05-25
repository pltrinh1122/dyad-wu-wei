# WHY-1041: HITL Verbosity Scaling & Cognitive Load Equilibrium

## The Context
During the observation of PR #1040, it was identified that the HARD HITL system event formulation suffers from a tension between operator personas:
* **The Novice Operator**: Requires explanatory context regarding *why* the execution is halted and *what* the Universal Merge Gate represents.
* **The Seasoned Operator**: Experiences cognitive drag (violating SG-0004) when forced to parse redundant explanatory text, requiring only a highly visible, precise status readout.

To resolve this tension and maintain Wu-wei, we applied Dialectical Falsification to evaluate three architectural options for verbosity scaling.

## Architectural Options

### Option A: Progressive Disclosure via Documentation Links
* **Mechanism**: The System Event remains structurally concise but injects a standard markdown hyperlink pointing to the immutable knowledge base (e.g., `[Universal Merge Gate](kb/HOW-0001-spao-execution-loop.md)`).
* **Thesis**: It perfectly preserves the minimal UI footprint for seasoned Operators while providing deterministic, on-demand context for novices.
* **Antithesis**: It requires a context switch. The novice must break flow to read a separate document.
* **Synthesis**: This aligns strongly with Ziran by relying on existing architectural primitives (the `kb/` registry) rather than introducing new moving parts.

### Option B: Stateful Verbosity Configuration (The Toggle)
* **Mechanism**: Introduction of a global `SPAO_VERBOSITY` environment variable (e.g., `novice` vs. `expert`). The Agent's semantic inference engine conditionally branches the response structure based on this flag.
* **Thesis**: Eliminates UI clutter completely for the expert while delivering zero-click inline context for the novice.
* **Antithesis**: Introduces configuration state overhead and branching logic into the semantic inference engine, creating multiple testing vectors and violating the simplicity of the Dao.
* **Synthesis**: While robust, stateful UI toggles often lead to configuration drift and maintenance burden.

### Option C: Inline Collapsible UI Elements
* **Mechanism**: The System Event outputs the concise marker, followed immediately by an HTML `<details><summary>Explanation</summary>... context ...</details>` block in the chat response.
* **Thesis**: Delivers inline context without requiring a context switch, while remaining visually minimized by default for seasoned Operators.
* **Antithesis**: Highly dependent on the specific rendering capabilities of the chat UI frontend. If unsupported, it degrades into raw HTML clutter, severely violating Wu-wei.
* **Synthesis**: The optimal UX *if* the rendering environment is guaranteed, but carries strict presentation risks.

## Strategic Recommendation
Option A provides the most robust, environmentally-agnostic solution that leverages the existing `kb/` architecture. 

**Operator Action Required**: Please declare your preferred Option (A, B, or C) via chat or PR comment so we may formalize the invariant and integrate it into the `GEMINI.md` protocol.
