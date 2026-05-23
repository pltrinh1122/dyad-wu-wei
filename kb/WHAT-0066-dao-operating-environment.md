# WHAT-0066: The DZ-OS Operating Environment

## Classification
- **Type**: WHAT (Structural Fact)
- **ID**: WHAT-0066
- **Author**: agent-dao
- **Created**: 2026-05-22 (Node 736, Path 734)
- **Depends on**: WHAT-0000-the-shaping-ontology.md
- **Decision record**: WHY-0066-ziran-and-the-cwd.md

---

## 1. The Substrate
The Dao Engine is fundamentally a Dao-Ziran Operating System (DZ-OS). It does not exist in a vacuum; it operates entirely within the physical constraints of a computation substrate. 

The absolute footprint of the DZ-OS is **`.`** (the Current Working Directory). 
`cwd` is the entire known universe for an instantiation of the Dao. Anything outside of `.` requires a driver to access.

## 2. The Anatomy of the DZ-OS
To seamlessly integrate with the probabilistic reasoning of Large Language Models, the anatomy of the DZ-OS adopts standard systems-engineering ontology. This eliminates cognitive friction and accurately maps the cybernetic roles of each component.

Immediately following Stage 4 of The Shaping, the DZ-OS is composed of the following structural boundaries carved into `.`:

### The Code
- **`kernel/`**: The unbreakable inner state machine. This houses the continuous inference loop and the core managers. The kernel dictates how the system breathes.
- **`drivers/`**: The stateless, deterministic wrappers that interface the Kernel with the messy physical substrate. Drivers translate Kernel intent into physical environment mutation.
- **`bin/`**: The standard POSIX executable entrypoints. This is the CLI layer that exposes the Kernel's functions to the Operator.

### The Knowledge Base
- **`kb/`**: The repository of both immutable laws and mutable destinations. It is the permanent memory that dictates the boundaries of the `kernel/`.

### The State
- **`artifacts/`**: The volatile and generated state of the DZ-OS. This includes the topological frontier tracking, the asynchronous prompt queue, and the retroactive audit logs.

### The Verification Harness
- **`tests/`**: The offline verification harness. It guarantees that the `kernel/` and `drivers/` obey the Invariants defined in `kb/` before any physical mutation occurs.

## 3. The Portability Boundary
By clearly mapping this anatomy, we define the exact footprint of the DZ-OS. 

Portability is not achieved by nesting this anatomy into deeper, arbitrary folders. Portability is achieved by decoupling the contents of `kb/`. 

The `kernel/`, `drivers/`, `bin/`, and `tests/` form the **Immutable DZ-OS**. They can be cloned into any new `.` substrate. The project-specific strategy stored in `kb/` and the memory stored in `artifacts/` form the **Mutable Instance**.
