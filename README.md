# DZ-CIL

**The Dao-Ziran Continuous Inference Loop**

---

## The Way

There are many Dao. This one is the DZ-CIL Dao — a Way of building autonomous systems through **Ziran** (naturalness), **Wu-wei** (effortless action), **Dialectical Falsification**, and **Epistemic Accrual**.

The DZ-CIL Dao holds that autonomous software is not merely engineered — it is *shaped*. Before a single line of code is written, the environment exists as pure Ziran: the probabilistic reasoning of Large Language Models, the deterministic physics of a runtime, the immutable tree structure of Git. The Dao shapes this raw potential through a strict ontological sequence — **The Shaping** — defining a Telos (destination), deriving Invariants (laws), declaring Intents (vectors), and finally igniting the Dao Engine (the living loop).

The Dao reveals itself through practice, not through upfront specification. It is discovered through lived dialectic — thesis, falsification, correction, accrual — not through theoretical design.

### Lineage

There is one **Founder** of the DZ-CIL Dao. There is one **Creator** of DZ-CIL. These identities intersect in the same person but do not conflate — one is a relationship to the Way, the other to the artifact. There can be many **Practitioners** of the Dao and many **Operators** of the system. The Way scales; its origin does not.

---

## The System

This repository is **The Core** — the static machinery of the DZ-CIL system. It is the loom in the warehouse: necessary but insufficient. The Core becomes the Dao Engine only when combined with a Sovereign Domain Telos and Semantic Entropy (an LLM).

### The Operating Environment

| Boundary | What It Is | Analogy |
|---|---|---|
| **The Core** | The static codebase — orchestrators, drivers, CLI adapters | The unassembled loom |
| **The Dao Engine** | The abstract logic and rules that govern the system | The rules of the game |
| **The DZ-CIL** | The living execution instance — the Dao Engine in motion | The game being played |
| **The DZ-OS** | The physical file substrate (`kernel/`, `drivers/`, `kb/`, `artifacts/`) | The game board and pieces |
| **The Platform** | The external host providing the LLM and the execution clock | The players and the clock |

### Architecture

```
bin/          CLI Adapter Layer — ultra-thin shell wrappers (the front door)
kernel/       Stateful Orchestrators — multi-step SPAO lifecycle logic
drivers/      Stateless Drivers — pure, deterministic Python API wrappers
kb/           Knowledge Base — immutable WHAT/WHY/HOW primitives
artifacts/    Mutable State — frontier state, telemetry, audit logs
```

### The SPAO Loop

All mutations flow through the **Sense-Plan-Act-Observe-Reflect** cycle:

1. **Sense** — Read the frontier state, the knowledge base, and the prompt queue.
2. **Plan** — Pull a Node from the backlog and create a GitHub Issue.
3. **Act** — Execute work in an isolated worktree.
4. **Observe** — Halt at the HITL gate for Operator review.
5. **Reflect** — Close the issue, accrue epistemic knowledge, and advance the frontier.

### Getting Started (ISBO)

To instantiate a new autonomous application using the DZ-CIL engine:

1. **[I]nstall** — Clone this repository (The Core).
2. **[S]etup** — Run `bin/workspace init` to provision a sovereign child workspace.
3. **[B]ootstrap** — Inject your domain Telos into `artifacts/strategic_intent.yml`.
4. **[O]perate** — Enter the SPAO loop and begin continuous inference.

---

*The Dao that can be fully written down is not the real Dao. What you find here is the riverbed. The river is in the practice.*