# Harmonize Node 2464: Mechanical Shell Closure Orchestration

## Goal
Enforce mechanical state transition upon CLI exit using a shell hook architecture that wraps the `agy` command and points it to our existing `./bin/status` router to trigger passive telemetry sweeps.

## Architectural Alignment
1. **Shell Hook Materialization**: Following the `dyad-cairn` architecture, we will establish `bin/dyad-shell-hooks.sh` that provides `agy_dyad()` and `claude_dyad()` aliases.
2. **Status Triggering**: The shell hook will trap the exit condition of the interactive CLI tool (`agy` or `claude`). When control is returned to the outer shell, the hook will programmatically evaluate if `./bin/status` exists in the local repository and immediately execute it. 
3. **Passive Sweeps**: Reusing the existing `./bin/status` executable fulfills the "Passive Ziran Auditor" pattern—ensuring that every CLI exit naturally drops the Operator into an updated state overview with all background daemons evaluated, and avoids the maintenance overhead of a dedicated `./bin/exit` script.

## Constraints & Invariants
- The implementation MUST reside in `bin/dyad-shell-hooks.sh`.
- The implementation MUST NOT attempt to execute `bin/status` if it does not exist (e.g., if the user executes the command outside the repository context).
- This aligns with SG-0003 (Preservation of Autonomous Velocity) by automating post-CLI telemetry sweeps directly in the shell.
