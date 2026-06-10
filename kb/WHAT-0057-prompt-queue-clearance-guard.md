# WHAT-0057: Prompt Queue Clearance Guard

## Purpose
To enforce the Synergistic Human-Agent Partnership by ensuring the agent pauses autonomous DAG execution whenever there are pending conversational prompts from the Operator. This prevents the Agent from silently progressing on tasks without acknowledging manual overrides or guidance provided through the `artifacts/prompt_backlog.yml` queue.

## Mechanism
A Lexical Guard (`CONVERSATIONAL_ALIGNMENT` HTIL Gate) MUST be injected into the primary state-machine transitions that acquire new workloads or synchronize the backlog structure:
1. `bin/node plan-start`
2. `bin/node sync-clean` (and `sync` wrapper)

### Invariant
Before these functions execute their primary logic, they MUST query the size of the pending prompt queue via `kernel.daemon_status.get_prompt_backlog_size()`. 

If the size is greater than 0:
1. The process MUST halt immediately with a non-zero exit code (`sys.exit(1)`).
2. The process MUST print a clear `[HTIL GATE ENGAGED: CONVERSATIONAL_ALIGNMENT]` warning instructing the user (or Agent) to run `bin/prompt process` before DAG execution can continue.

### Exemption
This guard does not restrict the Agent from completing its currently active Node lock (e.g., executing `plan-finish`, `checkout`, or `reflect`). It strictly limits the initiation of **new** lock acquisitions or **system-wide synchronizations**, ensuring the current step can gracefully conclude while blocking autonomous continuation.
