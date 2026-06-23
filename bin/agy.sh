#!/bin/bash
SESSION_NAME="agy"
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
            gh issue create --title \"[BUG] Daemon Crash (\$SESSION_NAME)\" --body \"Daemon exited with \$EXIT_CODE. Stderr:
\`\`\`
\$(cat $LOG_FILE)
\`\`\`\"
            echo 'Sleeping 60s before restart...'
            sleep 60
        else
            sleep 5
        fi
    done"
    tmux attach-session -t "$SESSION_NAME"
fi
