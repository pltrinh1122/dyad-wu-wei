# WHAT-0592: CLI Persona Alignment Gates Design

## 1. Intent
To enforce the agent persona ownership boundaries at the CLI runtime level, preventing unauthorized agents from executing Nodes (e.g., `plan-start`, `checkout`) that belong to Strategic Goals they do not own.

## 2. Technical Design

### A. The Validation Gate
A new validation gate `validate_persona_alignment(node_id, spao_persona_id)` will be introduced (e.g., in `kernel/daemon_strategic.py` or a dedicated `kernel/persona_gate.py`). 
This gate will:
1. Lookup the Strategic Goal (SG) of the target `node_id`.
2. Parse `kb/WHAT-0062-agent-persona-ownership-index.md` to resolve the `owner_persona` for that SG.
3. Compare `owner_persona` to the executing `SPAO_PERSONA_ID`.
4. If they do not match (and `owner_persona` is not `shared`), the gate MUST `sys.exit(2)` (fail-closed) with a clear unauthorized violation message.

### B. CLI Integration
The alignment gate will be integrated directly into the state transition actions in `kernel/node_lifecycle.py` and invoked during:
- `plan-start`
- `checkout`
- `reflect` (optional safety check)

### C. Falsification & Observability
If a node belongs to an `unassigned` SG, the gate will fail-closed. This forces the Dyad to formally register the SG to a persona before work can begin.

## 3. Feedforward Activities
1. `agent-platform` will build the Python parsing utility for `WHAT-0062`.
2. `agent-meta` will wire the gate into the CLI lifecycle hooks.
