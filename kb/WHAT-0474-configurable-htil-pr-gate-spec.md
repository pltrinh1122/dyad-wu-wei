# WHAT-0474: Operator Configurable Gate Enforcement Specification

## 1. Overview
This specification formalizes the technical materialization for the "Operator Configurable Gate Enforcement" logic as outlined in `WHY-0473`. It enables the Operator to dynamically define a set of "sacred files" that trigger a Hard HITL block during PR reflection, defaulting the remaining files to a risk-managed autonomous merging pathway.

## 2. Configuration Schema
The configuration will be injected into the repository-level `dyad-wu-wei.yml` file under the `governance` block.

```yaml
governance:
  spao_purity_enforcement: true
  sacred_files:
    - GEMINI.md
    - DYAD.md
```

### Parsing Rules
* **Absence:** If the `sacred_files` array is missing or empty, the system MUST default to the foundational identity files: `["GEMINI.md", "DYAD.md"]`.
* **Evaluation:** Exact path matching or filename matching will be utilized. If any file in the `git diff` output for the PR matches an entry in the `sacred_files` list, the PR MUST drop into the Hard HITL wait-state.

## 3. Component Modifications

### `kernel/node_lifecycle.py`
Locate the `Evaluate Administrative Node HTIL Bypass` logic inside the `reflect()` function (approx. line 591):

1. Use the standard `yaml` parser to open and read `dyad-wu-wei.yml` from the root of the repository (`main_repo` context).
2. Extract the `sacred_files` list, falling back to `["GEMINI.md", "DYAD.md"]`.
3. Iterate over the `modified_files` (obtained from `git_client.diff_names()`).
4. If `any(f in sacred_files for f in modified_files)`, set `is_autonomous_merge = False`.

### Test Harness (`tests/`)
1. Add unit tests in `tests/test_node_lifecycle.py` (or similar test file) to mock the YAML configuration and assert that the HTIL bypass logic correctly honors the `sacred_files` directive.
2. Ensure the fallback behavior remains intact when `dyad-wu-wei.yml` lacks the directive.

## 4. Operational Invariant
The system must NEVER automatically merge changes to its core execution loop definitions (`GEMINI.md`/`DYAD.md`) unless explicitly overridden by the Operator via the removal of those files from the `sacred_files` list. The default state must always be secure (Fail-Safe).


## 5. Portability Axiom Justification
The enforcement of HTIL gates (specifically the Hard HITL block for sacred identity files like `GEMINI.md` and `DYAD.md`) is directly anchored to the **Portability Axiom**. The Dyad relies on text-based lexical markers (e.g., `lean!`, `lean.`, `clip.`) within the git ecosystem and prompt interface rather than proprietary UI buttons or platform-specific autonomy authorization tools. By isolating these sacred files and managing their drift through strict operator gates, we ensure the agent's identity and execution logic remain universally portable across different foundational LLMs without being compromised by engine-specific "auto-merge" or proprietary state mechanisms.
