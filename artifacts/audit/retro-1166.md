# Retrospective 1166: Checkout Branch Name Failure

## Context
During the execution of Node 1166, the Agent executed the `checkout` command without providing the required `branch_name` positional argument:
`SPAO_PERSONA_ID=frontier ./bin/node checkout 1166`

## Failure
The `daemon_node.py` script rejected the invocation with `error: the following arguments are required: branch_name`, and subsequently telemetry logged a `FAILURE` event.

## Resolution
The Agent learned that `checkout` requires both the node ID and the branch name, and that the branch name must conform to the invariant: `node/<id>-<kebab-case>`.
The command was successfully re-issued as `SPAO_PERSONA_ID=frontier ./bin/node checkout 1166 node/1166-ratify-healing-protocol`.

## Prevention
Agents must supply the strictly formatted branch name when executing checkout, e.g., `SPAO_PERSONA_ID=frontier ./bin/node checkout 1166 node/1166-ratify-healing-protocol`.
