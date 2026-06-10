# Steering Taxonomy for CSI Guards

When designing CSI (Consistency) Guards, the steering provided to the Agent must be strictly categorized based on the failure mode. This taxonomy dictates when to use Declarative vs. Imperative steering.

## 1. Declarative Steering (The "What must be true")
* **Failure Mode:** Cognitive, Environmental, or Logical breaches (e.g., Tests failing, Remote GAP failing, Audit DAG unresolved).
* **Rule:** State the invariant condition that must be satisfied, not the commands to achieve it.
* **Why:** The path to remediation is unknown and highly contextual. Declarative steering grants the Agent maximum autonomy to dynamically determine *how* to achieve the required state, preventing rigid, sub-optimal paths.
* **Example:** `[STEERING VECTOR] The Intent Gate requires the remote GAP environment to actively fail. The Agent must satisfy this invariant before advancing.`

## 2. Imperative Steering (The "How to fix it")
* **Failure Mode:** Strict Mechanical or Tooling bottlenecks (e.g., Linter formatting, missing RCA artifact file, locked Retro).
* **Rule:** Provide the exact tool or mathematical path required to unblock the state.
* **Why:** There is literally only one physical way to resolve the blockage. Declarative steering (e.g., "The lockfile must not exist") risks the Agent bypassing tooling (e.g., `rm lockfile`) rather than executing the required process (`./bin/retro`). Imperative commands act as the required paved road.
* **Example:** `[STEERING VECTOR] You must resolve the retro and physically execute \`./bin/retro\` to unlock.`

## 3. The Telemetry Invariant
**Autonomy without telemetry is just guessing.** 
For declarative steering to function, the Agent must be able to read the physical state of the failure. Every CSI Guard must aggressively print its underlying exhaust (stdout, stderr, stack traces, specific failing node IDs) to the terminal *before* emitting the Steering Vector. 
If a guard swallows its logs, it mathematically blinds the Agent, forcing a manual diagnostic cycle and violating the division of labor.

### The Exhaust Classification (Inline vs Deferred)
Not all exhaust must be emitted inline. The guard must classify its exhaust to minimize token noise:
1. **Transient or Computed Truths (Must Emit Inline):** If the failure is subject to environmental drift (e.g., Remote GAP) or relies on internal guard logic (e.g., parsing the Audit DAG), the exact state at the moment of failure is unique telemetry. The guard **must** dump the exhaust inline before the steering vector.
2. **Highly Reproducible Tooling (Must Defer):** If the failure is entirely deterministic and reproducible via local physical binaries (e.g., `pytest`, linters), the guard possesses zero unique telemetry. The guard should **not** dump the exhaust inline. Instead, it must defer the diagnostic phase by explicitly providing the reproduction command in the steering vector (e.g., `[STEERING VECTOR] ... Run 'pytest -q --tb=short' to isolate the failing assertions.`).
