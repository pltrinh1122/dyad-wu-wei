# Retrospective: Node 952 Plan Start Failure (Dependency Violation)

## Failure Detail
*   **Command**: `SPAO_PERSONA_ID=frontier ./bin/node plan-start 952`
*   **Error**: `Dependency Violation: Node #952 depends on Node #951, which is still open!`
*   **Context**: Under the Triple-Node Doctrine, Node 952 (Reflect Activity) depends on Node 951 (Plan Probe). Since Node 950 and Node 951 were redundant and bypassed in favor of custom Probes A and B, they were left in an `OPEN` state. Trying to lock Node 952 triggered a dependency check failure because the predecessor nodes were not closed.

## Codified Insight
When custom Probes are spawned to resolve a Path's scope in lieu of boilerplate Triple-Node Probe templates, the boilerplate Probes (Harmonize/Plan) must be formally closed or marked resolved in the backlog before attempting to lock the terminal Reflect Activity.

## Mitigation Action
1. Close Node 950 and Node 951 on GitHub via `github_client.close_issue()`.
2. Check off the corresponding items in Path 949's issue body.
3. Lock Node 952 and execute checkout.
4. Document the dependency resolution in this retro record (`retro-922.md` / `retro-952.md`).
