import sys
import subprocess
from kernel.daemon_telemetry import record_execution

@record_execution(stage="skill")
def run_git_command(args: list[str]) -> int:
    """Executes a git command via the ./bin/git wrapper."""
    res = subprocess.run(["git"] + args)
    return res.returncode

def main():
    sys.exit(run_git_command(sys.argv[1:]))

if __name__ == "__main__":
    main()
