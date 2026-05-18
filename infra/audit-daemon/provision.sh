#!/bin/bash
set -e

echo "Starting Audit Daemon Provisioning..."

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CONFIG_FILE="$REPO_ROOT/infra/audit-daemon/audit_config.yml"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file not found at $CONFIG_FILE"
    exit 1
fi

# Extract timer_interval using grep and awk
TIMER_INTERVAL=$(grep "timer_interval:" "$CONFIG_FILE" | awk -F'"' '{print $2}')
if [ -z "$TIMER_INTERVAL" ]; then
    # Fallback if no quotes
    TIMER_INTERVAL=$(grep "timer_interval:" "$CONFIG_FILE" | awk '{print $2}')
fi

if [ -z "$TIMER_INTERVAL" ]; then
    echo "Error: Could not parse timer_interval from config. Defaulting to 5m."
    TIMER_INTERVAL="5m"
fi

echo "Configured Timer Interval: $TIMER_INTERVAL"

echo "Generating User-Level Systemd Service..."
mkdir -p ~/.config/systemd/user

cat <<EOF > ~/.config/systemd/user/audit-daemon.service
[Unit]
Description=Antigravity Audit Daemon Service
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/env python3 $REPO_ROOT/skills/audit_daemon.py
WorkingDirectory=$REPO_ROOT
EOF

cat <<EOF > ~/.config/systemd/user/audit-daemon.timer
[Unit]
Description=Antigravity Audit Daemon Timer

[Timer]
OnBootSec=5m
OnUnitActiveSec=$TIMER_INTERVAL

[Install]
WantedBy=timers.target
EOF

echo "Enabling and starting daemon..."
systemctl --user daemon-reload
systemctl --user enable audit-daemon.timer
systemctl --user start audit-daemon.timer

echo "Provisioning Complete. The audit-daemon timer is now active."
