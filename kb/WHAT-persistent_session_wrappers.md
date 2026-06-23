# Plan for Node #2434: Persistent Session Wrappers

## Objective
Create `bin/agy.sh` and `bin/claude.sh` to run the `audit_daemon.py` in a persistent `tmux` session, decoupling the daemon heartbeat from the LLM and adhering to the "Dark Substrate" invariant.

## Implementation Details
1. **tmux Wrapper Script (`bin/agy.sh` & `bin/claude.sh`)**:
   - Check if a `tmux` session named `agy` (or `claude`) exists.
   - If not, create a new detached session.
   - Inside the session, run an infinite `while` loop:
     - Execute `python3 drivers/audit_daemon.py` and redirect `stderr` to a temporary log file.
     - Capture the exit status code.
     - If the exit code is non-zero (crash), execute `gh issue create --title "[BUG] Daemon Crash (<session_name>)" --body "$(cat <log_file>)"` to serialize the bug into the backlog.
     - Sleep before restarting (e.g., 60 seconds on crash, 5 seconds on normal exit).
   - Attach to the session.

## Shell Script Blueprint
```bash
#!/bin/bash
SESSION_NAME="agy" # or "claude" for claude.sh
LOG_FILE="/tmp/${SESSION_NAME}_daemon_err.log"

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Session $SESSION_NAME already exists. Attaching..."
    tmux attach-session -t "$SESSION_NAME"
else
    echo "Creating new session $SESSION_NAME..."
    tmux new-session -d -s "$SESSION_NAME" "while true; do
        echo 'Starting audit_daemon.py...'
        python3 drivers/audit_daemon.py 2> $LOG_FILE
        EXIT_CODE=\$?
        if [ \$EXIT_CODE -ne 0 ]; then
            echo 'Daemon crashed with exit code '\$EXIT_CODE'. Creating bug report...'
            gh issue create --title \"[BUG] Daemon Crash (\$SESSION_NAME)\" --body \"Daemon exited with \$EXIT_CODE. Stderr:\n\`\`\`\n\$(cat $LOG_FILE)\n\`\`\`\"
            echo 'Sleeping 60s before restart...'
            sleep 60
        else
            sleep 5
        fi
    done"
    tmux attach-session -t "$SESSION_NAME"
fi
```

## Next Steps
- Implement the bash scripts in `bin/agy.sh` and `bin/claude.sh`.
- Ensure they are made executable (`chmod +x`).
- Test that crash interception creates an issue as intended.
