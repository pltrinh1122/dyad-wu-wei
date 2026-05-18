import os
import subprocess

def run_tests(target: str = "tests/") -> int:
    """Executes pytest within the virtual environment, streams output, and returns exit code."""
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    env["ANTIGRAVITY_RUNNING_TESTS"] = "1"
    
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
        env=env
    )
    
    return result.returncode
