# WHAT-0066: The Dao OS Operating Environment (DZ-OS Anatomy)

## Classification
- **Type**: WHAT (Structural Fact)
- **ID**: WHAT-0066
- **Author**: agent-dao
- **Created**: 2026-05-22 (Node 736, Path 734)
- **Depends on**: WHAT-0000-the-shaping-ontology.md
- **Decision record**: WHY-0066-ziran-and-the-cwd.md

---

## 1. The Substrate
The Dao Engine is fundamentally a Dao Operating System (DZ-OS). It does not exist in a vacuum; it operates entirely within the physical constraints of a computation substrate. 

The absolute footprint of the Dao OS is **`.` (the Current Working Directory)**. 
`cwd` is the entire known universe for an instantiation of the Dao. Anything outside of `.` requires a driver to access (e.g., a network request to GitHub, a path traversal to `/tmp/`).

## 2. The Anatomy of the Dao OS (Maximum Ziran)
To seamlessly integrate with the probabilistic reasoning of Large Language Models (Ziran), the anatomy of the Dao OS adopts standard systems-engineering ontology. This eliminates cognitive friction and accurately maps the cybernetic roles of each component.

Immediately following Stage 4 of The Shaping, the Dao OS is composed of the following structural boundaries carved into `.`:

### The Sensory & Actuation Layer (The Code)
- **`kernel/`**: The unbreakable inner state machine. This houses the continuous inference loop (the SPAO loop) and the core managers (Frontier, Transaction, Telemetry). The kernel dictates *how* the system breathes.
- **`drivers/`**: The stateless, deterministic wrappers that interface the Kernel with the messy physical substrate. Drivers include the GitHub API client, Git binary wrappers, and the File Locker. They translate Kernel intent into physical environment mutation.
- **`bin/`**: The standard POSIX executable entrypoints. This is the CLI layer that exposes the Kernel's functions to the Operator.

### The Physics & Vectors (The Knowledge)
- **`kb/` (Knowledge Base)**: The repository of both immutable laws (Invariants) and mutable destinations (Telos, Intents). It is the permanent memory that dictates the boundaries of the `kernel/`.

### The Active State (The Memory)
- **`artifacts/`**: The volatile and generated state of the Dao OS. This includes the topological frontier tracking (`frontier_state.md`), the asynchronous prompt queue, and the retroactive audit logs. It is the RAM of the system.

### The Verification Layer
- **`tests/`**: The offline Verification Harness. It guarantees that the `kernel/` and `drivers/` obey the Invariants defined in `kb/` (such as `WIP-N=1`) before any physical mutation occurs.

## 3. The Portability Boundary
By clearly mapping this anatomy, we define the exact footprint of the Dao OS. 

"Portability" is not achieved by nesting this anatomy into deeper, arbitrary folders (e.g., wrapping it all in a `dao/` folder). Portability is achieved by decoupling the *contents* of `kb/`. 

The `kernel/`, `drivers/`, `bin/`, and `tests/` form the **Immutable Dao OS**. They can be cloned into any new `.` substrate. The project-specific strategy stored in `kb/` and the memory stored in `artifacts/` form the **Mutable Instance**.
