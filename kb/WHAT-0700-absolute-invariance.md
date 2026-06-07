# WHAT-0700: The Absolute Invariance of the Audit Ledger

## 1. The Principle
The **Absolute Invariance of the Audit Ledger** principle dictates that history, once written into the system's ledger (`artifacts/audit/` and git commit history), MUST NEVER be retroactively altered, rebased out of existence, or semantically destroyed.

## 2. Why it matters (The Void Context)
In an autonomous system where physical memory is ephemeral, the Audit Ledger is the single source of truth for the systemic identity (the "Dao"). If the ledger can be rewritten, the system's perception of reality can be silently gaslit. This creates catastrophic cascading failures in the Continuous Inference Loop, as learning models require absolute trust in the immutability of past state transitions to deduce correct future transitions.

## 3. Structural Axioms

### Axiom 1: Additive-Only State
The `artifacts/audit/` directory is an append-only store. Existing retrospective documents MUST NOT be modified or deleted. Errata or corrections MUST be appended as new delta documents.

### Axiom 2: Cryptographic Causality
Every execution node must trace its causality back through an unbroken chain of Merkle root hashes (git history). Rebasing `main` or force-pushing over historical nodes is strictly classified as an existential threat to systemic integrity and is expressly forbidden.

### Axiom 3: Immutability of the Dao
Changes to the core engine rules (`GEMINI.md`, `kb/`) must be thoroughly audited. Past rules may be marked deprecated, but their historical context must survive in the commit history to explain past agentic behaviors.

## 4. Operational Boundaries
- **Prohibited Actions**: `git push --force` to `main`, squashing commits after they merge to `main`, or deleting files in `artifacts/audit/`.
- **Permitted Actions**: Amending commits on an active `node/*` branch *before* the reflection phase completes; deprecating rules by creating a new `WHAT`/`HOW` that supersedes the old one.
