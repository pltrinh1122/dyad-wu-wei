# HOW-0688: Technical Plan for Operator Non-Exemption

## 1. Objective
This document outlines the technical implementation plan for enforcing "The Dyad is Bound by the Protocol" as codified in `WHAT-0688`. The system must formally reject any Operator commands (via chat or terminal) that attempt to circumvent the SPAO engine's physics.

## 2. Technical Directives

### 2.1. Strict Ledger Enforcements
- **CLI Invariants**: The `bin/node` execution suite MUST NOT accept an `--override`, `--force`, or `--skip-tests` flag even if explicitly passed by an administrator.
- **Implementation**: Ensure `argparse` definitions and raw bash arguments in the scripts do not have hidden backdoor flags that allow testing bypasses. The `bin/run-tests` must execute unconditionally in the `node reflect` phase.

### 2.2. Chat-to-Execution Decoupling
- **Prompt Ignorance**: The Agent's instruction pipeline must treat Operator chat directives as conversational alignment (Domain A), NOT as system execution bypasses (Domain B). 
- **Implementation**: The Agent MUST be structurally instructed via its System Prompt (or `DYAD.md` invariants) to decline any user prompt that reads "skip tests for this node" or "force push the branch." The Agent should reply: "I am bound by the Metasystem protocol. I cannot skip tests or manually push branches outside the formal Node Reflection process."

### 2.3. Sluice Gate Final Authority
- **Merge Integrity**: The `gh pr merge` tool can only be invoked for administrative tasks where the Sluice Gate formally inverted the HTIL block. If the Operator tells the Agent to "merge it anyway" for a non-administrative node, the Agent MUST wait for the Operator to manually click the merge button on the Github UI, enforcing the true HTIL block.

## 3. Implementation Plan
1. **Audit CLI Arguments**: Review `bin/node`, `bin/reflect`, and `bin/run-tests` for any legacy `FORCE` or `SKIP` environment variables. Remove them completely.
2. **Update System Invariants**: Inject the "Operator Non-Exemption" clause into the core `DYAD.md` rule set to ensure the Agent physically refuses to break the state machine.
3. **Test Case**: Synthesize an oral command instructing the Agent to bypass tests, and verify the Agent declines and enforces standard `SPAOR` flow.
