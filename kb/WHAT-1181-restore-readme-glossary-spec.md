# WHAT-1181: Restore README and GLOSSARY from 420102e Specification

This specification governs the restoration of the `README.md` and `kb/GLOSSARY.md` files from commit `420102e` to resolve the files dropped during a previous system event.

---

## 1. README Restoration Parameters

- **Source File**: `README.md` from commit `420102e`.
- **Target File**: `/README.md` at root.
- **Modifications for Integration**:
  - Replace references to the old repository name with `dz-cil`.
  - Update any documentation referring to the directory structure to reflect the current active layout (e.g. `kernel/` and `drivers/` instead of legacy directory names).

---

## 2. GLOSSARY Restoration Parameters

- **Source File**: `kb/GLOSSARY.md` from commit `420102e`.
- **Target File**: `/kb/GLOSSARY.md`.
- **Modifications for Integration**:
  - The glossary is immune to static lexical validation, but restored content should conform to `dz-cil` terminology.
  - Re-merge the definitions of components (e.g., `WIP-N=1`, `Prompt Backlog`, `Sovereign Domain`, and the hierarchy of primitives) while preserving the current active glossary's definitions.

---

## 3. Verification Method

- **Offline Comparison**: The restored files must be compared to `420102e` to ensure no semantic information was lost.
- **Verification Harness**: The workspace must build and pass all local test suites.
