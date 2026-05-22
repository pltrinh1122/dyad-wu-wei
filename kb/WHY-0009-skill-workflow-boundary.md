# WHY-0009: Skill vs. Workflow Boundary & Interface Classification

## 1. Context
As the `agent-antigravity` execution loops (`SPAO`, `NL`, `PML`) matured, ambiguity arose between what constitutes a **Skill** (`drivers/`), a **Workflow** (`kernel/`), and the wrapper shell scripts (`bin/`). 

Specifically, during a PML architectural evaluation (Probe 41), it was identified that `drivers/flow_state_manager.py` manages stateful, multi-step Node-Loop phase transitions (e.g., closing issues, checking out branches, and enforcing SPAO rules). Concurrently, the `bin/` directory had become a critical operator interface without a formal classification in the Core Paradigm.

## 2. Decision

We codify the following architectural boundaries to eliminate conceptual ambiguity:

1. **Skill (Stateless Primitives):** A pure, atomic, deterministic callable. It maintains zero state between invocations, has no SPAO/NL stage awareness, and maps to a single external system interaction. Independently testable. All Skills belong in `drivers/`.
2. **Workflow (Stateful Orchestration):** A multi-step, stage-aware orchestration sequence. It sequences Skills across NL phase transitions and maintains active state context. Workflows belong in `kernel/`.
3. **CLI Adapter Layer (`bin/`):** Thin interface shell scripts that bridge human operators and agent intent to the underlying `drivers/` or `kernel/` layers. `bin/` is NOT a core execution pillar; it is an I/O interface boundary.

## 3. Consequences

* **Misclassification Acknowledged:** `drivers/flow_state_manager.py` is formally recognized as a Workflow misclassified as a Skill. It will be migrated to `kernel/flow_state_manager.py` in a subsequent execution Node.
* **Lexical Clarity:** `GLOSSARY.md` and `WHAT-0001-agentic-architecture.md` are updated to explicitly define the **Skill** vs. **Workflow** boundary and the `bin/` interface classification.
* **Testing Integrity:** By ensuring `drivers/` contains only pure atomic functions, we maintain 100% isolatable test coverage in `tests/`. State-machine logic in `kernel/` will require integrated flow testing.
