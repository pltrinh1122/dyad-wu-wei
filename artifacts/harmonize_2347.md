# Harmonize Node 2347: System Crash in reflect

## Root Cause Analysis
The system crash occurred during the `reflect` phase execution:
```
FileNotFoundError: [Errno 2] No such file or directory: '.../.worktrees/node/2335-reflect-nba/artifacts/audit/retro-2335.yml'
```
This happened because `bin/node reflect` defines an optional positional argument `frontier_file` (as the 7th argument) in `kernel/daemon_node.py`:
`parser_r.add_argument("frontier_file", nargs="?", default="artifacts/frontier_state.md")`

When agents attempt to provide extra arguments (like attaching a retro artifact directly via a positional argument), `argparse` consumes it as `frontier_file`. The framework then mistakenly attempts to load the frontier state from the passed file (e.g., `artifacts/audit/retro-2335.md`), resolving it to `.yml` and failing with a `FileNotFoundError` or `StateCorruptionError`.

## Proposed Solution
To prevent agents from accidentally passing incorrect files as `frontier_file` via trailing positional arguments, we should convert the `frontier_file` argument in `kernel/daemon_node.py` from an optional positional argument to a named flag (e.g. `--frontier-file`). 

Specifically, in `kernel/daemon_node.py`:
Change:
`parser_r.add_argument("frontier_file", nargs="?", default="artifacts/frontier_state.md")`
To:
`parser_r.add_argument("--frontier-file", default="artifacts/frontier_state.md")`

We should also apply this change to the `cancel` subcommand, which uses the same pattern.
`parser_c.add_argument("frontier_file", nargs="?", default="artifacts/frontier_state.md")` -> `parser_c.add_argument("--frontier-file", default="artifacts/frontier_state.md")`

And in `cmd_reflect` and `cmd_cancel`, update the references to match the new argument name if needed (argparse automatically converts `--frontier-file` to `args.frontier_file`).

This approach gracefully resolves the issue without breaking the standard 6-argument invocation pattern defined in `DYAD.md`.
