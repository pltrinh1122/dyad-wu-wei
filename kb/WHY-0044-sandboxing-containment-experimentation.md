# WHY-0044: Sandboxing and Containment Experimentation — Architectural Decisions

## Context & Rationale
To enable safe, gateless autonomous execution (SG-0002), the agent's runtime environment must be isolated from the host environment. Unrestricted execution poses risks of side-effects such as:
1. Accessing or exfiltrating sensitive credentials (e.g. host SSH keys, AWS credentials, custom environment tokens).
2. Deleting, mutating, or corrupting files on the host filesystem outside the active repository.
3. Spawning runaway processes that exhaust system CPU or memory resources (denial of service).
4. Initiating unauthorized network outbound connections to unknown or unsafe IP addresses.

We need a design that guarantees containment boundaries while allowing standard git manipulations, local testing, and command invocation.

---

## Architectural Options

### Option 1: Process-Level Isolation (Bubblewrap / `bwrap`)
- **Concept**: Use Linux user namespaces, mounting `proc`, `sys`, and read-only host directories like `/usr` and `/lib`, while mounting the workspace as read-write, and denying network access using network namespaces.
- **Pros**:
  - Extremely fast startup (<5ms) and native execution speed.
  - No daemon dependency (Docker daemon is not required).
  - Simple git tree synchronization without mounting overhead.
- **Cons**:
  - Requires Linux namespaces and bubblewrap (`bwrap`) command installed on the host.

### Option 2: Container-Level Isolation (Docker / Podman)
- **Concept**: Execute all operations inside an ephemeral container. Limit egress using `--network none`.
- **Pros**:
  - High popularity, mature ecosystem, works across OS platforms.
  - Complete filesystem isolation.
- **Cons**:
  - High startup latency (~500ms per command).
  - Heavy credential/SSH mounting complexity.
  - Requires docker daemon running and configured.

---

## Evaluation Matrix

| Vector | Option 1 (Bubblewrap) | Option 2 (Docker Container) |
| :--- | :--- | :--- |
| **Startup Overhead** | ⭐️⭐️⭐️ (<5ms latency) | ⭐️ (500ms+ latency) |
| **Credential Safety** | ⭐️⭐️⭐️ (Home dir blackboxed) | ⭐️⭐️⭐️ (No home dir mount) |
| **Network Egress Containment**| ⭐️⭐️⭐️ (No-network namespace) | ⭐️⭐️⭐️ (`--network none`) |
| **Filesystem Isolation** | ⭐️⭐️ (Read-only host system mounts) | ⭐️⭐️⭐️ (Complete image isolation) |
| **Resource Limits (CPU/Mem)** | ⭐️⭐️ (Can set via cgroups/prlimit) | ⭐️⭐️⭐️ (Docker native limits) |

---

## Proposed Direction

We will proceed with a **Hybrid Sandboxing Approach**:
1. **Primary Local Runner**: Bubblewrap (`bwrap`) for rapid inner-loop testing and containment checks, avoiding daemon overhead.
2. **Standardized Container Integration**: Ephemeral Docker containers for cloud deploy runs.

We will focus our containment rules on specifying the filesystem mounts, CPU/memory resource allocations, and network constraints.
