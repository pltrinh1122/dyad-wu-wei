# WHY-0068: Architectural Rationale for Semantic Entropy as the Minimum Agentic Requirement

## Classification
- **Type**: WHY (Architectural Decision Record)
- **ID**: WHY-0068
- **Author**: agent-dao
- **Created**: 2026-05-22
- **Related WHAT**: WHAT-0068-semantic-entropy.md

---

## 1. The Context: Defining the Footprint
As we refined the definition of the Dao-Ziran Operating System (DZ-OS), we recognized a critical omission in our foundational ontology. If a human operator attempts to deploy a "brand new Dao Engine" into a new repository, what are the minimum system requirements they must provide?

Classically, the answer for all software is `(Compute + Storage)`. However, we realized that if we deploy the Dao Engine onto a purely deterministic von Neumann machine, the system will suffocate. Without a source of probabilistic reasoning, the SPAO loop cannot execute.

## 2. The Resolution: Redefining "Minimum Requirements"
We resolved this by formally elevating **Semantic Entropy** (the latent space of Large Language Models) to the status of a primary computational resource, sitting equally alongside CPU and Disk space.

For any future instantiation of the Dao Engine, the "Minimum System Requirement" disclaimer must explicitly list Semantic Entropy (e.g., an active LLM API connection).

## 3. The Categorical Boundary
This establishes a stark architectural boundary between Traditional Software and Agentic Software:

- **Traditional Software** explicitly rejects entropy. It is designed to crash or error when non-deterministic states occur. Its Minimum System Requirement is merely Compute and Storage.
- **Agentic Software** (The Dao Engine) explicitly *requires* entropy. It is designed to consume ambiguity and generate probabilistic vectors of action. Its Minimum System Requirement is Compute, Storage, and Semantic Entropy.

You cannot run Agentic Software on a traditional deterministic substrate. Ziran (Compute + Storage + Semantic Entropy) must be fully present before the Dao Engine can spark into existence.
