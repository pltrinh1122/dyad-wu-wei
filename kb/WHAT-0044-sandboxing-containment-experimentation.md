# WHAT-0044: Sandboxing and Containment Experimentation — Specification

## 1. Process-Level Sandbox Rules (Bubblewrap)

To run a task under process-level sandboxing, the executor must invoke bubblewrap (`bwrap`) with the following arguments:

- **Filesystem Isolation**:
  - `--ro-bind /usr /usr`: Mount system binaries and libraries read-only.
  - `--ro-bind /lib /lib` and `--ro-bind /lib64 /lib64`: Mount linker and libraries read-only.
  - `--ro-bind /bin /bin` and `--ro-bind /sbin /sbin`: Mount executable paths read-only.
  - `--ro-bind /etc /etc`: Mount configurations read-only.
  - `--bind /tmp /tmp`: Mount temporary directories as read-write.
  - `--bind {WORKSPACE_DIR} {WORKSPACE_DIR}`: Mount active workspace root as read-write.
  - `--dir /home/pt`: Sandbox or stub user home directory to prevent reading SSH keys or private profile files.

- **Network Egress Containment**:
  - `--unshare-net`: Restrict network access completely, leaving only loopback interface.

- **Process Namespace Isolation**:
  - `--unshare-pid`: Isolate PID space so the agent cannot send signals to or view host system processes.

---

## 2. Container-Level Sandbox Rules (Docker)

To run a task under container-level sandboxing, the executor must run Docker with:

- **Egress Restrictions**:
  - `--network none`: Disable container networking.

- **Resource Constraints**:
  - `--memory 2g`: Hard limit container RAM usage to 2GB.
  - `--cpus 2.0`: Limit container execution to 2 CPU cores.

- **User Privilege Limits**:
  - `--user 1000:1000`: Run as non-root user (matching local host UID/GID).
  - `--read-only`: Set the container rootfs as read-only, allowing writes only to designated volume mounts.

---

## 3. Verification & Compliance Policies

1. **Local Test Compliance**:
   - Every sandboxed execution must pass an initial TDD cycle inside the isolated workspace using `./bin/run-tests`.
2. **Network Egress Check**:
   - The metasystem audit daemon must actively monitor subprocess socket calls and block executions attempting to connect to external endpoints.

## Verification & Status
- **Status**: Locked
- **Verified by**: Node 435 Plan Probe
- **Reflected by**: Node 436 Reflect Activity

