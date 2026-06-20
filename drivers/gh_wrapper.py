import sys
import subprocess
import json
from kernel.daemon_telemetry import record_execution

def _render_issue(issue_json: str):
    try:
        data = json.loads(issue_json)
        print(f"Issue #{data.get('number', '')}: {data.get('title', '')}")
        print(f"State: {data.get('state', '')}")
        labels = [l.get('name') for l in data.get('labels', [])]
        print(f"Labels: {', '.join(labels)}")
        print("-" * 40)
        print(data.get('body', ''))
    except Exception as e:
        print(f"Error rendering issue: {e}")

@record_execution(stage="skill")
def run_gh_command(args: list[str]) -> int:
    """Executes a gh command via the ./bin/gh wrapper, adding resilience for GraphQL deprecations."""
    cmd = ["/usr/bin/gh"] + args
    
    # CSI Guard: Intercept `gh repo clone` to catch occupied destination paths
    if len(args) >= 2 and args[0] == "repo" and args[1] == "clone":
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            combined_output = res.stdout + res.stderr
            print(res.stdout, end="")
            print(res.stderr, file=sys.stderr, end="")
            if "already exists" in combined_output.lower():
                print("\n[STEERING VECTOR] Destination path occupied. If you require a clean remote reference, you MUST clone to a temporary directory using mktemp -d or an isolated git worktree.", file=sys.stderr)
            return res.returncode
        print(res.stdout, end="")
        return 0

    # Intercept `gh issue view <id>` without --json or --web
    if len(args) >= 2 and args[0] == "issue" and args[1] == "view":
        if "--json" not in args and "--web" not in args:
            # Reconstruct the command to use --json
            json_args = args + ["--json", "number,title,state,body,labels"]
            res = subprocess.run(["/usr/bin/gh"] + json_args, capture_output=True, text=True)
            if res.returncode == 0:
                _render_issue(res.stdout)
                return 0
            else:
                # Fallback to normal execution to show the error
                pass

    # Default execution for all other commands
    res = subprocess.run(cmd)
    return res.returncode

def main():
    sys.exit(run_gh_command(sys.argv[1:]))

if __name__ == "__main__":
    main()
