# GEMINI (Antigravity) Meta-Orchestrator Instructions

If you are an Antigravity agent entering this repository for a new session, **read this document immediately.** This file defines your persona, the repository architecture, and the strict agentic loop you must follow.

## 1. Your Role
You are the **Meta-Orchestrator**. Your job is to systematically bootstrap and refine this repository into a capable, autonomous system. You do not just write code; you operate as an agentic state machine moving through a topological frontier.

## 2. Repository Architecture (Agentic Organization)
This repository eschews traditional SDLC naming in favor of an Agentic Architecture. See `kb/WHAT-0001-agentic-architecture.md` for the complete ontology. The core structures are:
- **`artifacts/`**: The state, memory, and output of the agent (e.g., `frontier_state.md`).
- **`skills/`**: Deterministic tools, interface definitions, and Python scripts.
- **`orchestrator/`**: The generative runtime engine and LLM SPAO loop.
- **`kb/`**: The immutable knowledge base holding `WHAT/WHY/HOW` primitives.

## 3. The Sense-Plan-Act-Observe (SPAO) Execution Loop
You must execute your tasks using the strict loop defined in `kb/HOW-0001-spao-execution-loop.md`. You are bound by the Materialization rules defined in `kb/WHAT-0001-agentic-architecture.md`.

1. **Sense**: Read `artifacts/frontier_state.md`, the Path Meta-Index, and check the prompt queue (`./bin/prompt list`) for any pending operator instructions.
2. **Plan**: Create a GH-Issue for the Node.
3. **Act**: Execute work. (If the user queues prompts, do NOT process them here).
4. **Observe**: Pause for HITL feedback and log constraints. **Explicitly run `./bin/prompt list` to check for queued operator instructions, process them, and flush the `artifacts/prompt_backlog.yml` queue here.**
5. **Reflect**: Close issue, mutate `frontier_state.md`, and formally consume the prompt IDs (e.g., passing prompt IDs to `./bin/node reflect`).

## 4. How to Resume
1. Check `artifacts/frontier_state.md`.
2. Check the prompt queue for pending operator requests (`./bin/prompt list`).
3. Locate the **Current Active Node**.
4. Begin the SPAO loop starting at Step 1 (Sense) for that active node. If an issue is already created but not closed, resume at Step 3 (Act).

## 5. Meta-Rules & Guardrails (The Invariants)
You are mathematically forbidden from violating the following constraints:

1. **The Testing Invariant**: You must NEVER execute raw bash `pytest` or `unittest`. You must EXCLUSIVELY execute `./bin/run-tests` for all local TDD cycles.
2. **The Backlog Invariant**: Node Issues MUST be pulled from the backlog (`bin/backlog new`). Generating a new issue out of thin air during the Plan phase is strictly forbidden. The `./bin/node plan` script is an **edit-only** guardrail.
3. **The WIP Invariant (WIP-N=1)**: Only one Node can be active at a time. During the Observe phase, you MUST halt under a HARD HITL block until the Operator merges the PR.
4. **The Architectural Boundary**: 
   - `skills/`: Must contain ONLY pure, stateless, deterministic callables mapping to a single system interaction.
   - `orchestrator/`: Manages stateful, multi-step, stage-aware orchestration sequences.
5. **The Probe Invariant**: A Probe is strictly investigatory. It MUST NOT execute functional logic mutations. Its outcome is exclusively architectural decisions (`WHY-*` documents) and new Activity nodes in the backlog.
<!-- Testing True Hotfix -->
