# WHAT-1668: Persona Gate Fallback Specification

## 1. Intent
To define a resilient fallback mechanism for dynamic persona resolution when the `SPAO_PERSONA_ID` environment variable is absent during node execution, preventing unhandled system crashes.

## 2. The Invariant
When a lifecycle script (such as `plan-start` or `sync`) is invoked and `SPAO_PERSONA_ID` is strictly absent from the environment:
1. The Persona Gate must NOT immediately raise a fatal exception.
2. The dynamic persona resolution mechanism must autonomously fall back to the registered Path or Node owner.
3. The system shall consult the agent persona ownership indices defined in `WHAT-0062` (Agent Persona Ownership Index) or `WHAT-0065` (Domain Path Ownership Index) to resolve the correct persona based on the target Node's domain or ID.

## 3. Falsification
The previous behavior, which caused an immediate system crash (`Persona Gate Blocked` exception) when `SPAO_PERSONA_ID` was omitted, is hereby formally falsified as it breaks autonomous chaining (e.g., when the `sync` process attempts to start an NBA in the background without explicitly inheriting the variable).

## 4. Scope
- Update `kernel/daemon_strategic.py` (specifically `_verify_persona`) to implement the owner fallback lookup before raising an exception.
