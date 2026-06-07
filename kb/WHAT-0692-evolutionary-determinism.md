# WHAT-0692: Evolutionary Determinism (Mutable Physics via Rigid Pipelines)

## 1. Principle Statement
**Evolutionary Determinism** dictates that the underlying "physics" of the system (the SPAOR loop, state constraints, locking mechanisms) are fully mutable, but they may only be mutated through the system's own formally rigid pipelines.

## 2. Rationale
If the Operator or Agent can manually hotfix the engine bypassing the execution loop (e.g. directly editing `bin/node` on the `main` branch), we break the fundamental invariant of continuous autonomous evolution. The pipeline used to upgrade the system must be the same pipeline used to execute normal paths.

## 3. Directives
- **Self-Hosting Metasystem**: The `dyad-wu-wei` system MUST use itself to upgrade itself. Any changes to CLI tools, CI scripts, or engine logic MUST traverse `Plan -> Checkout -> Act -> Reflect`.
- **Pipeline Dogfooding**: The rigid pipeline is the *only* vector for mutable physics. Manual commits to the execution logic are formally classified as a systemic failure.
