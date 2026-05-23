# HOW-0078: Passive Ziran Auditor Implementation

## 1. Context
Following the philosophical specification in `WHAT-0077`, this document defines the physical implementation schema for the Passive Ziran Auditor. The Auditor is a continuous, off-band process that parses execution telemetry and adjusts the Daoist gradients (`Laminar`/`Turbulent`) of Knowledge Base (`kb/`) primitives.

## 2. Telemetry Ingestion (The Event Stream)
To observe the "wake" of an Agent's execution, we implement a structured telemetry log. 

### Data Store
- **File**: `artifacts/telemetry/events.jsonl`
- **Format**: Append-only JSON Lines.

### Event Schema
Whenever an Agent completes a Node, encounters a friction point (crash), or undergoes an Audit hook, `daemon_telemetry.py` must append a record:
```json
{
  "timestamp": "2026-05-22T21:44:48Z",
  "node_id": "759",
  "event_type": "AUDIT_HOOK_TRIGGERED",
  "status": "TURBULENT",
  "kb_target": "SG-0005",
  "context": "Failed to supply SPAO_PERSONA_ID"
}
```

## 3. The Central KB Ledger (`artifacts/kb_ledger.yml`)
Rather than injecting YAML frontmatter into every individual Markdown file inside `kb/` (which generates significant Git churn and pollutes pure documentation), the Metasystem will maintain a singular Central Ledger for Gradients.

### Schema
```yaml
primitives:
  WHAT-0077:
    state: Active
    gradient: Laminar
    confidence: 1.0
  WHY-0076:
    state: Active
    gradient: Laminar
    confidence: 0.95
  SG-0005:
    state: Active
    gradient: Turbulent
    confidence: 0.40
```

## 4. The Gradient Engine (`kernel/ziran_auditor.py`)
A new pure function module will be introduced to process the event stream and mutate the ledger.

### Execution
1. The engine reads the trailing $X$ events from `events.jsonl`.
2. It aggregates events grouped by `kb_target`.
3. It applies the scoring formula: $\delta = \frac{S}{S+T}$, where $S$ is Laminar completions and $T$ is Turbulent events.
4. If $\delta > 0.9$, the primitive is marked `Laminar`. If $\delta < 0.6$, the primitive is marked `Turbulent`.
5. It overwrites `artifacts/kb_ledger.yml` with the newly calculated gradients.

## 5. Implementation Sequence
The corresponding Backlog Activities must implement these layers sequentially:
1. `Activity 763`: Modify `daemon_telemetry.py` to write `events.jsonl`.
2. `Activity 764`: Create `kernel/ziran_auditor.py` for mathematical calculation of gradients.
3. `Activity 765`: Implement the mutation logic in `kernel/ziran_auditor.py` that reads/writes `kb_ledger.yml`.
