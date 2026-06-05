# WHAT-1784: System Crash Invariants (Systematic Hardening Spec)

## 1. Intent
Derived directly from the Root Cause Analysis in `WHY-1784-system-crash-rca.md`, this specification defines the four foundational invariants required to systematically harden the engine against the classes of crashes observed during Path 1567. 

This document serves as the architectural SPEC for the Systematic Hardening of System Crash Boundaries (Path 1783).

## 2. The Four Invariants of Explicit Verification

To eliminate implicit trust and enforce structural resilience, the following invariants are now codified into the Wu-wei Dao:

### I. The Sandbox Pre-Condition Invariant
**Context:** Derived from Git Switch Conflicts (Node 1531).
**Definition:** The kernel_daemon MUST NEVER execute a repository state transition (e.g., checkout, switch, rebase, reset) without first explicitly validating the topological safety of the sandbox. 
**Enforcement:** Rather than catching exceptions *during* a git operation, the engine must assert that the worktree is pristine *before* attempting the transition. If the pre-condition fails, the kernel_daemon must abort and yield gracefully rather than crashing mid-transition.

### II. The Strict Data Contract Invariant
**Context:** Derived from Prompt Daemon Initialization failure (Node 1572).
**Definition:** Un-validated or loosely typed data MUST NEVER cross the boundary between persistent disk storage and daemon execution memory.
**Enforcement:** All state files (e.g., `artifacts/prompt_backlog.yml`, `artifacts/frontier_state.yml`) must pass through a strict schema validation layer upon loading. If the schema contract is violated, the daemon must raise a structured, operational error (e.g., `SchemaValidationError`) rather than failing downstream with a generic `KeyError` or `TypeError`.

### III. The Fault Containment Invariant
**Context:** Derived from Validation Gate Escapes (Node 1579).
**Definition:** The core SPAO execution loop MUST act as a fault-tolerant supervisor. No child component, script, or validation gate shall have the execution authority to seize or crash the macro-kernel_daemon.
**Enforcement:** All peripheral executions (hooks, gates, sensors) must be wrapped in a universal containment layer (a top-level try/catch or supervisor block). If a child faults, the supervisor must intercept the unhandled exception, map it to an operational failure event (e.g., `[🚫 BLOCKED]`), and cleanly exit or rollback the transaction.

### IV. The Subprocess Abstraction Invariant
**Context:** Derived from GitHub GraphQL Deprecation Noise (Node 1641).
**Definition:** The engine MUST NEVER invoke external CLI binaries directly via raw `subprocess` calls without an isolating SDK layer.
**Enforcement:** All interactions with external tools (e.g., `gh`, `git`) must pass through an abstraction layer that:
1. Cleanly isolates structured payload data (e.g., `stdout` formatted as JSON).
2. Explicitly decouples and safely logs execution noise (e.g., `stderr`).
3. Explicitly manages and translates non-zero exit codes into operational Domain objects rather than generic `CalledProcessError` exceptions.

## 3. Implementation Phasing
This SPEC establishes the architectural goals. The actual implementation of these invariants (the code) will be deferred to subsequent nodes on Path 1783. The Operator holds the explicit authority to review and disposition this SPEC before any implementation begins.
