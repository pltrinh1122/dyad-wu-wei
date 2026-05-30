#!/bin/bash
set -e

echo "Starting GitHub Actions Runner Provisioning..."

RUNNER_DIR="$HOME/actions-runner"
mkdir -p "$RUNNER_DIR"
cd "$RUNNER_DIR"

# Download runner binary if it doesn't exist
if [ ! -f "config.sh" ]; then
    echo "Downloading GitHub Actions Runner binary..."
    curl -o actions-runner-linux-x64-2.316.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.316.1/actions-runner-linux-x64-2.316.1.tar.gz
    tar xzf ./actions-runner-linux-x64-2.316.1.tar.gz
    rm actions-runner-linux-x64-2.316.1.tar.gz
fi

echo "Fetching secure registration token via gh api..."
# We explicitly set the repo name so gh api works even outside the git dir
TOKEN=$(gh api -X POST repos/pltrinh1122/dyad-wu-wei/actions/runners/registration-token --jq .token)

if [ -z "$TOKEN" ]; then
    echo "Failed to fetch registration token. Ensure gh CLI is authenticated."
    exit 1
fi

echo "Configuring runner..."
# Use --unattended to avoid interactive prompts
./config.sh --url https://github.com/pltrinh1122/dyad-wu-wei --token "$TOKEN" --unattended --replace || true

echo "Generating User-Level Systemd Service..."
mkdir -p ~/.config/systemd/user
cat <<EOF > ~/.config/systemd/user/github-runner.service
[Unit]
Description=GitHub Actions Runner
After=network.target

[Service]
ExecStart=$RUNNER_DIR/run.sh
WorkingDirectory=$RUNNER_DIR
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

echo "Enabling and starting daemon..."
systemctl --user daemon-reload
systemctl --user enable github-runner
systemctl --user start github-runner

echo "Bootstrapping CI Python venv..."
VENV_DIR="$RUNNER_DIR/venv"
REQUIREMENTS="$(cd "$(dirname "$0")" && pwd)/../../requirements-dev.txt"
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --quiet -r "$REQUIREMENTS"
echo "CI venv ready at $VENV_DIR"

echo "Provisioning Complete. The daemon is now a permanent resident of your host OS."
