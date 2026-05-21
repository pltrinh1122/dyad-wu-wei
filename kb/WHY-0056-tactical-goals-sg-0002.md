# WHY-0056: Architectural Rationale for SG-0002 Tactical Goals

## 1. Context & Architectural Challenge

Strategic Goal **SG-0002** (Gateless Autonomous Execution within Risk-Managed Sandbox) requires that the agent can execute changes autonomously without a manual human gatekeeper. However, granting execution authority raises significant safety concerns:
1.  **System Integrity**: Malicious or buggy command executions could overwrite critical files, leak credentials, or destabilize the host system.
2.  **Resource Contention**: Infinite loops or memory-hogging processes could freeze the agent workspace or local machine.
3.  **Verification Drift**: Uncommitted or dirty worktree states lead to untracked side-effects that contaminate subsequent runs.
4.  **Trust Transition**: The transition from manually gated interaction to full autonomy is not binary; a middle-ground is required to prevent premature risk exposure.

To address these without violating **SG-0003** (Preservation of Autonomous Velocity - requiring offline tests to run in <60 seconds), we must design lightweight, granular containment layers guided by strict rubrics.

---

## 2. Rationale for Tactical Goal (TG) Selection Invariants

To prevent the accumulation of ad-hoc or poorly defined goals, we establish four formal selection invariants matching the governance standards applied to Strategic Goals:

### 2.1 INVARIANT_TG_FALSIFIABLE_VERIFICATION (TG-Axiom 1)
*   **Rationale**: If a containment mechanism cannot be programmatically proven to block or fail on a violation, we cannot trust it autonomously. Every TG must define a binary test check. If we cannot write a failing test for it, it remains a purely decorative claim and is rejected.

### 2.2 INVARIANT_TG_DIRECT_RISK_MITIGATION (TG-Axiom 2)
*   **Rationale**: Tactical goals must solve real-world relationship bottlenecks. We must not waste resource budget refactoring elements for aesthetic or modular reasons under the guise of safety. Every TG must map directly to a documented risk surface of the parent SG.

### 2.3 INVARIANT_TG_INNER_LOOP_PURITY (TG-Axiom 3)
*   **Rationale**: Isolation mechanisms are useless if they slow execution down so much that the operator bypasses them. We must avoid heavy containers or VM layers that violate SG-0003. Containment must happen via low-overhead local OS APIs (namespaces, cgroups, local git structures).

### 2.4 INVARIANT_TG_ENFORCEMENT_GRADIENT (TG-Axiom 4)
*   **Rationale**: Operator trust is built incrementally. A binary "all-or-nothing" switch forces operators to keep manual checks active indefinitely out of caution. A gradient allows testing rules in monitor/dry-run mode, giving the operator real safety statistics before enabling strict blocks.

---

## 3. Design Decisions & Trade-Offs

### 3.1 Compute Containment: Local Namespaces vs. Full VM Isolation
*   **Decision**: Implement process-level sandboxing using Linux namespaces, `cgroups`, or lightweight sandboxing wrappers (such as `systemd-run` or `firejail`) rather than virtual machine (VM) isolation.
*   **Rationale**:
    *   *VM Isolation*: Restricting execution to a clean virtual machine (or heavy Docker containers with full OS stacks) guarantees maximum isolation. However, booting and mounting the workspace in a fresh VM on every command run introduces seconds of latency, violating the SG-0003 constraint.
    *   *Local Containment*: Leveraging Linux process containment primitives adds negligible execution overhead, preserving fast local TDD cycles.
*   **Trade-Off**: Process-level namespaces share the host kernel and are theoretically less secure than hardware-level VM isolation, but the performance gains are critical for the agent's inner loop velocity.

### 3.2 Network Containment: Firewall Hooks vs. Mock Enforcement
*   **Decision**: Restrict egress network requests at the execution boundary using socket-level filters or private network namespaces (`unshare -n` or custom proxy gates), rather than relying solely on library mocks.
*   **Rationale**: Library-level mocks (e.g. mocking `requests` or `urllib` in Python) are easily bypassed by direct shell invocations or compiled binaries. Intercepting network requests at the system level ensures absolute egress control.
*   **Trade-Off**: Setting up system-level network namespaces requires specific permissions or wrapping, which can complicate development setup. We mitigate this by using helper script wrappers.

### 3.3 File System Hardening: Copy-on-Write vs. Git Transactions
*   **Decision**: Rely on Git worktrees, checkout state checks, and automated `git clean` hooks to ensure filesystem state idempotence, rather than a copy-on-write (CoW) disk filesystem.
*   **Rationale**: Git is already the core state synchronization engine of the metasystem. Leveraging Git operations avoids system-level filesystem dependencies (like ZFS/Btrfs snapshots) and guarantees that any file mutation can be tracked, checked, and reverted using standard, portable VCS tools.
*   **Trade-Off**: If an agent executes commands that modify files outside the git repository structure, Git-based rollback cannot detect it. We mitigate this by strictly restricting the sandbox's writable working directory.

### 3.4 Gradual Autonomy: Binary Gating vs. Dynamic Gradual Gating
*   **Decision**: Implement operator-controlled dynamic gating (`TG-0002-06`) via configuration options, allowing the operator to selectively ungate low-risk domains first.
*   **Rationale**: The operator's trust in the agent's autonomy is built gradually. Binary (all-or-nothing) gating forces the operator to either stay manually involved in every simple change, or accept high risks on complex changes. A dynamic gate structure enables incremental trust delegation.
*   **Trade-Off**: A dynamic gating layer adds complexity to the state engine, which must now evaluate the target gate status (e.g., block vs. notify) before executing steps. We mitigate this by integrating it cleanly into the existing `HookManager`.

---

## 4. Alternative Approaches Considered

### 1. Traditional Single-Piece Flow (HITL Gates Only)
*   *Why rejected*: Keeps the operator in the loop for every single change. This does not scale and directly violates the North Star collaboration gap (NS-0001).

### 2. Full Containerized TDD Environments (Docker-in-Docker)
*   *Why rejected*: Heavy overhead and complex nesting in CI. It would violate the requirement to run validation test suites in under 60 seconds.
