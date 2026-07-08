# Plan: Intent-Alignment & Issue-Gated Lifecycle (Sense Loop)

## Overview
This plan implements the dyadically converged **"No-Self-Ratification"** invariant. It strictly bifurcates the Agent's workflow into an explicit **Sense (Elicitation) Phase** and an **Act (Execution) Phase**, using GitHub Issue labels as the state machine. The Agent cannot jump from prompt directly to execution; it must formalize its interpretation as an issue and await Operator ratification.

## Architectural Mapping (From `dyad-chiron` to `dyad-wu-wei`)
We will implement the following Issue state transitions using labels:
1. `status:clarify` : The issue is created from a raw intent.
2. `status:dispose` : The Agent has successfully played back its interpretation (intent + invariants) to the Operator.
3. `status:execute` : The Operator has explicitly approved the interpretation.

## Implementation Steps

### Step 1: Backlog Intake (`kernel/daemon_backlog.py`)
- Modify `BacklogDaemon.add()`: When creating an `intent` or `path` issue, replace the assignment of `status: todo` with `status:clarify`.
- Ensure new items naturally drop into the `clarify` bucket to signify they require intent-alignment.

### Step 2: The Agent's Elicitation Command (`bin/backlog converge`)
- Add a new `converge` command to `bin/backlog` (and `BacklogDaemon`).
- **Functionality**: `bin/backlog converge <issue_id>` will transition the issue from `status:clarify` to `status:dispose`.
- **Usage**: The Agent will run this command immediately after it replies in chat with its intent/invariant playback to signify that the Sense phase has converged on the Agent's side.

### Step 3: The Execution Gate (`kernel/node_lifecycle.py`)
- Modify `TerminalNode.plan_start()` to act as the hard gate.
- **Assertion**: Before acquiring a node lock (or checking out a branch), `plan_start()` MUST assert the presence of the `status:execute` label.
- **Failure Condition**: If the node possesses `status:clarify` or `status:dispose`, `plan_start()` will immediately exit with a `StateDissonanceError` or standard `sys.exit()`, citing: `[🚫 BLOCKED] Intent-Alignment Violation: Node has not been ratified. Expected 'status:execute'.`

### Step 4: The Operator Ratification Command
- Add `bin/backlog ratify <issue_id>` (or just use `set-status <id> status:execute`).
- This allows the Operator (or the Agent, on the Operator's explicit chat approval) to flip the label from `dispose` to `execute`.

## Invariant Adherence
- **No-Self-Ratification**: The Agent physically cannot begin executing (`plan-start`) an issue unless it has crossed into `status:execute`.
- **Dormancy**: If the Agent attempts to execute an unratified intent, the script will crash, halting the loop and dropping the Agent into True Dormancy until the Operator resolves it.
