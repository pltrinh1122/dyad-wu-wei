# WHY-0952: Boilerplate Probe Closure Prerequisite

## 1. Context & Problem Statement
Under the Triple-Node Doctrine, a typical execution path requires three nodes: a Harmonize Probe, a Plan Probe, and a Reflect Activity.
In certain scenarios, a Path's scope is resolved through custom Probes (e.g., Probe A, Probe B) in lieu of the standard boilerplate Harmonize/Plan Probes. 
When this occurs, the boilerplate Probes may remain unexecuted and `OPEN` in the backlog. If an agent subsequently attempts to `plan-start` the terminal Reflect Activity, the execution will crash with a `Dependency Violation` because the predecessor probes (the boilerplate Harmonize/Plan nodes) are still considered pending by the system's topological dependency checks.

## 2. Codified Insight
To maintain strict topological integrity and prevent dependency violations, any bypassed or redundant boilerplate Probes MUST be formally closed or marked resolved in the backlog before attempting to lock the terminal Reflect Activity.

## 3. Mitigation & Operational Rule
When custom Probes are utilized to fulfill a Path's planning phase:
1. The Agent or Operator must explicitly close the unused boilerplate Harmonize/Plan nodes on GitHub.
2. The corresponding list items in the parent Path's Meta-Index must be checked off to signal topological completion.
3. Only after the predecessors are resolved may the Reflect Activity be initiated via `bin/node plan-start`.
