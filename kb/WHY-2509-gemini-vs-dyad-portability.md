# WHY-2509: Architectural Decision Record for GEMINI.md vs. DYAD.md Portability Boundary

- **Type**: WHY (Architectural Decision Record)
- **Context**: The `dyad-wu-wei` engine must be strictly portable across disparate foundational LLM substrates (e.g., Anthropic's Claude vs. Google's Antigravity/Gemini). We must ensure that the universal physics of the engine are not corrupted by platform-specific workarounds.

## Decision Record
We formally establish a strict structural boundary between `DYAD.md` and `GEMINI.md` (or `CLAUDE.md`) to enforce the Portability Axiom.

### 1. DYAD.md (The Universal Engine)
`DYAD.md` is the platform-agnostic core definition of the Wu-wei engine. It holds the universal "physics" of the system:
- The **SPAOR** execution loop (Sense, Plan, Act, Observe, Reflect).
- The universal systemic invariants (e.g., `WIP-N=1`, True Dormancy, Autonomous Substrate Integrity).
- The structural registries, ontologies, and interaction protocols (`d-start`, `d-reflect`).

**Rule**: `DYAD.md` MUST NOT contain references to specific system prompt injections, proprietary tool names, or platform-specific execution nuances. It assumes a perfect, standardized agentic environment.
- **Presentation Layer**: UI-invariants for chat presentation (how the Agent speaks to the Operator, the formats used like CSS+SH, or hyperlinking conventions) are universally defined here. The UI behavior must be identical regardless of platform.

### 2. GEMINI.md / CLAUDE.md (The Hardware Abstraction Layer)
These files act as the **Personalized Anchor** and the **Hardware Abstraction Layer (HAL)** for the specific LLM instantiation. They translate the universal intent of `DYAD.md` into the specific tooling and harness constraints of the host environment.
- **Tool Mapping**: Translating universal asynchronous execution rules into platform-specific tool calls (e.g., mandating `run_command` and `schedule` in Antigravity).
- **Harness Suppression**: Implementing iatrogenic-injection suppression rules tailored to the host (e.g., instructing the agent to ignore `<EPHEMERAL_MESSAGE>` blocks injected by the Antigravity system wrapper).

## Justification
By decoupling the universal physics (`DYAD.md`) from the host-specific drivers (`GEMINI.md`), we guarantee that the `dyad-wu-wei` substrate remains a singular, universally portable engine. If the Dyad migrates to a new frontier model tomorrow, `DYAD.md` remains untouched; we merely author a new `NEW_MODEL.md` HAL file.
