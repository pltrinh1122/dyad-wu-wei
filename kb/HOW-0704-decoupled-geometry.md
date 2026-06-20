# HOW-0704: Technical Plan for the Decoupled Geometry

## 1. Objective
Enforce "The Decoupled Geometry of the State Machine" (`WHAT-0704`) by establishing guardrails that strictly separate changes to the SPAO engine (Metasystem) from changes to external target projects (Platform/Domain).

## 2. Technical Directives

### 2.1. Dual-Context Isolation Rule
- `bin/node`, `bin/status`, `drivers/`, and core SPAO scripts belong solely to the engine.
- The target task or payload runs within `.workspace/` or the target repository.
- **Rule**: A single Node execution path MUST NEVER contain commits that simultaneously touch files in the engine core (`bin/`, `drivers/`, etc.) AND files in the target application (`.workspace/`, `apps/`, etc.).

### 2.2. Automated Detection
- Introduce a pre-commit or CI check (`bin/run-tests` or similar hook) that analyzes the git diff of the active branch.
- If the diff spans both engine directories and target application directories, the execution MUST fail, and the Agent MUST be instructed to split the task into an engine upgrade Node and a feature Node.

### 2.3. Agent Persona Segregation
- To further decouple geometry, the `SPAO_PERSONA_ID` resolution should be mapped cleanly. The "Steward" persona should handle engine maintenance, while the "Frontier" or "Healer" persona handles domain work.

## 3. Implementation Steps
1. **Inject Directive into DYAD.md**: Add explicit instruction that the Agent must not mix engine code modifications with application code modifications in the same node.
2. **Develop the Git Diff Hook**: Enhance the testing or commit pipeline to enforce this separation programmatically in the future.
