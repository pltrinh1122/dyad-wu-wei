# Retrospective - Node 2490 (Intent Node Support)

## Summary
The Operator noted that raw intent was being ingested directly via `gh issue create`, which bypassed the backlog taxonomy and resulted in missing the `intent` label entirely. This was due to `bin/backlog new` not supporting an `intent` type.

## Actions Taken
- Edited `kernel/daemon_backlog.py` to recognize `intent` as a valid formal node type.
- Applied the `Intent: ` title prefixing rule.
- Added explicit label injection for `intent`, `status: todo`, and the standard `node` and `backlog` labels when this node type is created.
- Fixed brittle hard-coded `add_label.call_count` tests in `tests/test_daemon_backlog.py` to safely accommodate the universally applied `node` labels.

## Next Steps
- The CLI command `./bin/backlog new intent "My Idea" "My Goal"` is now formally supported, allowing clean ingestion of raw user intents directly from the CLI or subagents.
