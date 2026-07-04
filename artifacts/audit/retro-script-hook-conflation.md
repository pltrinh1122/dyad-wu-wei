# Retro: Script vs Hook Conflation (CSS+SH)

## STOP
- **Agent**: Conflating the execution payload with the delivery vehicle. When instructed to "remove all of the hooks", I deleted the mechanical spine scripts (`bin/standup.sh` and `bin/standdown.sh`) themselves, rather than just deleting the mechanisms that automatically triggered them (`agy`, `claude`, `.claude/settings.json`, and `bin/dyad-shell-hooks.sh`). 

## START
- **Agent**: I must recognize that `bin/standup.sh` and `bin/standdown.sh` are autonomous, substrate-agnostic steps invoked by the `d-start` and `d-reflect` disciplines. Removing an automated trigger does not render the underlying mechanical check obsolete; it merely shifts the invocation responsibility from the shell/system to the Agent's autonomous execution loop.

## CONTINUE
- **Agent**: Creating a formal retro immediately upon receiving a logic-error correction from the Operator (Rule 6).

## SH (Should Hold)
- **Operator**: "why did you interpret bin/standup.sh and bin/standdown.sh as hooks? they're autonomous steps in the d-start and d-reflect discipline."
