# WHY: Exhaust Logger Primitive

## 1. The Context
In the continuous operation of the Dao-Ziran Continuous Inference Loop (DZ-CIL), CSI Guards assert structural invariants before allowing execution to proceed. When a guard fails (e.g., Remote GAP validation or node label verification), it outputs the telemetry of that failure.

Currently, this telemetry (exhaust) is printed directly to stdout/stderr.

## 2. The Physical Vulnerability (Exhaust Dissipation)
If a guard merely `print()`s transient exhaust inline, that telemetry is volatile. 
- Terminal buffers can truncate it.
- LLM context windows might drop it.
- The environment may drift immediately after the guard trips.

When the exhaust dissipates, the Agent is physically blinded. It is given a Declarative Steering Vector (e.g., "The Remote GAP failed"), but it has lost the exact error trace that proves *why* it failed.

## 3. The Resolution: Survivor/Exhaust Logger
To harden the feedback loop, we must introduce an `ExhaustLogger` primitive that survives the crash.

1. **Durable Serialization**: Transient exhaust must be dumped to a physical file (e.g., `artifacts/audit/exhaust_<guard_name>.log`) before the system halts.
2. **Pointer Steering**: The steering vector emitted to the Agent must point directly to this serialized file, removing the reliance on volatile terminal buffers.
3. **Autoclear**: Upon successful remediation and re-validation, the passing guard autonomously purges the old exhaust artifact to prevent historical contamination.

This approach physically grounds the telemetry, ensuring the Agent always has precise, immutable data to reason over.
