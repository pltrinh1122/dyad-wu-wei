# WHAT-1669: Persona Gate Fallback Implementation Plan

## 1. Intent
To define the technical implementation details for the Persona Gate Fallback mechanism introduced in WHAT-1668.

## 2. Technical Scope
- Modify `kernel/daemon_strategic.py`: `_verify_persona`
- Load ownership indices (`WHAT-0062` and `WHAT-0065`) to perform dynamic persona resolution.

## 3. Fallback Logic
1. Attempt to read `SPAO_PERSONA_ID` from the environment.
2. If absent, retrieve the active Node ID from `artifacts/frontier_state.md`.
3. If no active Node is found, or if resolution fails, then raise the original exception.
4. If an active Node is found, query its metadata and map it to an owning persona via the ownership indices.
