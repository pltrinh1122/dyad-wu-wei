import os
import subprocess

def run_tests(target: str = "tests/") -> str:
    """Executes pytest within the virtual environment and returns the output."""
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    
    # Resolve the correct pytest executable dynamically
    venv_dir = os.environ.get("VIRTUAL_ENV")
    if venv_dir and os.path.exists(os.path.join(venv_dir, "bin/pytest")):
        pytest_exe = os.path.join(venv_dir, "bin/pytest")
    elif os.path.exists("/home/pt/actions-runner/venv/bin/pytest"):
        pytest_exe = "/home/pt/actions-runner/venv/bin/pytest"
    elif os.path.exists(".venv/bin/pytest"):
        pytest_exe = ".venv/bin/pytest"
    else:
        pytest_exe = "pytest"
        
    result = subprocess.run(
        [pytest_exe, target],
        env=env,
        capture_output=True,
        text=True
    )
    
    # If tests fail, pytest returns a non-zero exit code.
    # We still want to return the output so the Agent can read the failures.
    if result.returncode != 0:
        return result.stdout + "\n" + result.stderr
        
    return result.stdout
