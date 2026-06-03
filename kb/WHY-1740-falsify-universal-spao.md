# WHY-1740: Falsification of Universal SPAO Application

## The Claim
The implicit assumption was that the `git-node` (SPAO) execution model serves as the universal interface for the entirety of the Human-Agent Dyadic practice, meaning all interactions, including conceptual design and alignment, must be piped through its `plan-start -> checkout -> act -> reflect` state machine.

## The Falsification
Applying the SPAO engine to the Dyadic Cycle (design/alignment) generates severe friction because it applies an **asynchronous execution mechanism** to a **synchronous discovery problem**:

1. **The Paradox of the Pre-Contract**: SPAO requires a `plan-start` contract (a GH Issue with a defined goal) *before* execution can begin. However, the exact purpose of a Dyadic design session is to *discover* the goal and shape the contract. Forcing design into SPAO requires writing a rigid contract just to give the agent permission to figure out what the contract should be.
2. **The WIP Invariant Collision**: SPAO strictly enforces the **WIP-N=1 Constraint** (locking execution to a single git worktree) to prevent cognitive dilution during implementation. Conversely, design sessions are inherently divergent and orthogonal (WIP-N=$\infty$). Locking a conceptual session into a single execution branch lobotomizes the ability to explore parallel ideas.
3. **Latency and Bandwidth Mismatch**: SPAO is designed for *Materialized Autonomy* (high-latency, disconnected, durable state mutations, True Dormancy). A design session requires *Synchronous Resonance* (low-latency, high-bandwidth conversational fluidity). 

Dog-fooding SPAO for the Dyadic Cycle provides zero structural learnings because SPAO was built to *replace* human execution, not to *facilitate* human brainstorming.

## The Survivor: Defining the Boundary & The Handoff
To eliminate this friction, we formally decouple the **Dyadic Cycle** from the **Autonomous Engine** and establish a strict boundary between them.

### Domain A: The Dyadic Cycle (The Generator)
* **State**: Lock-free, synchronous, conversational. The SPAO engine is intentionally bypassed.
* **Function**: Dialectical brainstorming, falsification, and alignment.
* **Output**: Immutable knowledge artifacts (`WHY-xxxx` and `WHAT-xxxx` documents) and `Path` specifications in the backlog.

### The Handoff (The Sluice Gate)
* The explicit boundary where conversation ends and execution begins.
* The Operator or Agent defines the boundary: *"The design is locked. Drop into the engine."*
* The Agent transitions from Domain A to Domain B by generating the final Path issue and allowing the Next-Best-Action (NBA) daemon to pick it up.

### Domain B: The Autonomous Engine (The Executor)
* **State**: Locked (WIP-N=1), asynchronous, `git-node` bounded, True Dormancy.
* **Function**: Autonomous materialization of the artifacts generated in Domain A.
* **Output**: Pull Requests, passing test suites, and merged code.
