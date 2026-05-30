# Retro 1478

## Failure Context
During the reflect phase, a JSONDecodeError occurred because the invariants array was passed using single quotes around the outer array instead of proper double quotes.

## Root Cause
Bash escaping caused invalid JSON strings to be passed to the `daemon_node.py` CLI.

## Remediation
Properly formatted the JSON string `["[x] GEMINI.md explicitly codifies the new Telos"]` and passed it safely.

## Systemic Prevention
Use valid JSON with double quotes for CLI arguments that expect JSON arrays.
