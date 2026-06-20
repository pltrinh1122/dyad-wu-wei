# WHY-0473: Operator Configurable Gate Enforcement

## 1. The Context
The Wu-wei SPAO execution loop historically enforced a **Hard HITL (Human-in-the-Loop) Block** on every Pull Request. The Agent was required to yield the turn and drop into true dormancy until the Operator reviewed and merged the PR. While this maintained strict Operator oversight over codebase mutations, it created significant friction and blocked autonomous velocity for administrative, documentation, or trivial structural changes.

## 2. The Catalyst
The Operator provided a standing directive: *"i give you standing permission to adjust the HTIL PR block to filter only on GEMINI.md/DYAD.md changes."*

This directive fundamentally shifts the Wu-wei Dyad from a "Verify All" model to a "Risk-Managed Sandbox" model (aligned with SG-0002). The Operator acknowledges that mutations to the Universal Dao (`GEMINI.md` / `DYAD.md`) alter the Agent's consciousness and systemic constraints, requiring strict Operator alignment. However, standard software engineering files (code, tests, docs) are safely encapsulated within the CI/CD test harness and do not strictly require human verification before merging.

## 3. The Alignment
We are formally adopting an **Operator-Configurable Gate Enforcement** architecture.

### Core Principles:
1. **The Dao is Sacred:** Any PR that modifies `GEMINI.md`, `DYAD.md`, or other core identity/policy files MUST trigger the traditional Hard HITL Block.
2. **The Sandbox is Autonomous:** Any PR that exclusively modifies functional logic, tests, or standard documentation (and passes all local CI/CD testing invariants) is eligible for **Autonomous Merging** by the Agent.
3. **Configuration over Hardcoding:** The list of "Sacred Files" that trigger HITL must be configurable, likely within a repository-level configuration file (e.g., `dyad-wu-wei.yml` or `node.yml`), allowing the Operator to dynamically adjust the system's risk aperture.

## 4. The Path Forward
This alignment will be materialized in the subsequent Plan and Act nodes. The technical implementation will require:
* Modifying the `node_lifecycle.py` and `github_client.py` orchestrators to dynamically inspect the `git diff` of a branch prior to reflection.
* Implementing logic to branch the execution flow during the `reflect` phase: Automerge vs. Yield.
