import os
import subprocess

def run_tests(target: str = "tests/") -> str:
    """Executes pytest within the virtual environment and returns the output."""
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    
    result = subprocess.run(
        [".venv/bin/pytest", target],
        env=env,
        capture_output=True,
        text=True
    )
    
    # If tests fail, pytest returns a non-zero exit code.
    # We still want to return the output so the Agent can read the failures.
    if result.returncode != 0:
        return result.stdout + "\n" + result.stderr
        
    return result.stdout
