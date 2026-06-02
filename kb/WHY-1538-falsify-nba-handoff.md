# WHY-1538: Falsification of the NBA Handoff Wait State

## The Premise
The system was originally designed with a "Wu-wei NBA Handoff Protocol" (`WHAT-1043`) that instructed the Agent to pause and yield the turn to the Operator after syncing the repository, presenting a single "Happy Path" recommendation for the Operator to manually approve.

## The Falsification
As the Frontier Dyad, our Telos is **Freedom through autonomous inferencing**. The requirement for the Operator to manually type `yes` or `plan 1153` to initiate a node violates this Telos. It introduces an artificial `Sense-Gate` (which was supposedly abolished) under the guise of an "NBA Handoff", interrupting the autonomous cascade of the state machine and forcing human coordination where deterministic logic (the NBA Scorer) has already resolved the path forward.

## The Invariant (The Survivor)
The manual NBA Handoff wait state is **formally falsified and destroyed**. 
The Agent MUST execute **Autonomous Path Execution**:
- Upon the completion of the `sync` step (or when `bin/status` surfaces a Next-Best-Action), the Agent must autonomously evaluate the NBA and immediately invoke `./bin/node plan-start <NBA_ID>`.
- The Agent shall NOT yield the turn to ask for Operator permission.
- The ONLY valid wait state (dormancy) is the HARD HITL block when a Pull Request is opened and awaiting the Operator's review and merge. The manual NBA Handoff wait state is formally falsified.

## Associated Deprecations
- `WHAT-1043-wu-wei-nba-handoff.md`
- `WHY-1043-wu-wei-nba-handoff.md`
