# WHAT-1748: Lean DM Protocol Integration

## Problem Statement
The dark substrate must support asynchronous, pull-based communication between independent dyad repositories (e.g., Frontier, Steward, Healer). Existing designs proposed external polling daemons, which violate lean principles and incur unnecessary overhead.

## The Axiom of Synchronous Harvesting
We posit that the dyad agent only needs to know about incoming Direct Messages (DMs) when it transitions between states or awakens from dormancy. Waking an agent arbitrarily mid-sleep merely to announce "you have mail" when it cannot act upon it is mathematically anti-lean. Therefore, the DM ingest cycle must be strictly coupled to the **Sense** phase of the SPAO engine.

## Architectural Specification
We will integrate the `falsify.py` inbox mechanism into the native `HookDaemon` execution lifecycle.

1. **Submodule Harmony**: The `commons` git submodule will be updated to fetch `commons/scripts/falsify.py`.
2. **Outbound Payload Structure**: The agent will persist outgoing DMs in the repository tree under a new `dm/` directory.
3. **Inbound Injection**: We will implement `execute_dm_inbox_hook` in `kernel/sense_hooks.py`. This hook will silently invoke `falsify.py inbox --me dyad-wu-wei`. If unread mail is detected, it will format a high-visibility alert block embedded directly in the output stream of `bin/node sync` and `bin/status`. 
4. **Configuration Mapping**: We will append the new `dm_inbox` hook to `dyad-wu-wei.yml`.

## Falsifiability
This implementation is strictly lock-free and daemon-less. The presence of any new `python3` or `bash` background process introduced solely to poll `falsify.py` constitutes an architectural violation and a failure of this specification.
