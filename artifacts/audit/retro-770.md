# Retrospective: Status Retrieval Latency Violation

## Violation
The Agent attempted to resolve a routine Operator request for "current status" by executing multiple probabilistic LLM tool calls (`view_file` on a 2000-line markdown ledger, evaluating `bin/prompt list` output, and evaluating `bin/node view`). This resulted in unacceptable temporal latency, violating **SG-0003 (Inner-Loop Velocity)** and **Axiom 3 (Materializability)**.

## Correction
The Operator asserted that no inferencing should be necessary for static state retrieval and challenged the Agent to falsify the claim that a deterministic skill is required.

## Codified Insight
The claim is robust and non-falsifiable. Retrieving state (active node, prompt queue length, daemon status) from flat files and static APIs is a pure mathematical function. Funneling this deterministic retrieval through a probabilistic LLM context window is an architectural anti-pattern that burns compute and latency. To align with our Axioms, this must be encapsulated into a stateless deterministic CLI adapter (`bin/status`) to provide a zero-latency dashboard.

## Action Items
1. Materialized `kb/WHY-0081-deterministic-state-retrieval.md` to permanently codify this invariant.
2. Queued a Path in the Backlog to implement `bin/status`.
