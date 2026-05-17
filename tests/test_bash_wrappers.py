import os
import subprocess
import pytest

def test_run_tests_wrapper():
    """Verifies the bin/run-tests shell script executes successfully."""
    # Prevent infinite recursion when this test runs as a child process of bin/run-tests
    if os.environ.get("ANTIGRAVITY_RUNNING_TESTS"):
        return
        
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/run-tests')
    assert os.path.exists(bin_path)
    
    # Run the shell script and verify it executes our pytest suite successfully
    try:
        res = subprocess.run([bin_path], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        raise
    assert res.returncode == 0
    assert "test session starts" in res.stdout
    assert "passed in" in res.stdout

def test_node_wrapper_usage():
    """Verifies bin/node prints usage when no arguments or invalid subcommands are passed."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/node')
    assert os.path.exists(bin_path)
    
    # No args
    res = subprocess.run([bin_path], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Usage:" in res.stdout

    # Invalid subcommand
    res = subprocess.run([bin_path, "invalid"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Unknown subcommand:" in res.stdout

def test_node_plan_subcommand_usage():
    """Verifies bin/node plan enforces argument counts and prints usage on errors."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/node')
    assert os.path.exists(bin_path)

    # plan subcommand needs at least 2 args
    res = subprocess.run([bin_path, "plan"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Usage:" in res.stdout

def test_node_reflect_subcommand_usage():
    """Verifies bin/node reflect enforces argument counts and prints usage on errors."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/node')
    assert os.path.exists(bin_path)

    # reflect subcommand needs at least 7 args
    res = subprocess.run([bin_path, "reflect"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Usage:" in res.stdout

def test_backlog_wrapper_usage():
    """Verifies bin/backlog prints usage when no arguments or invalid subcommands are passed."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/backlog')
    assert os.path.exists(bin_path)
    
    # No args
    res = subprocess.run([bin_path], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Usage:" in res.stdout

    # Invalid subcommand
    res = subprocess.run([bin_path, "invalid"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Unknown subcommand:" in res.stdout

def test_backlog_subcommand_usage():
    """Verifies bin/backlog subcommands enforce argument counts and print usage on errors."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/backlog')
    assert os.path.exists(bin_path)

    # new subcommand needs at least 2 args
    res = subprocess.run([bin_path, "new"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Usage:" in res.stdout

    # view subcommand needs at least 1 arg
    res = subprocess.run([bin_path, "view"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Usage:" in res.stdout

    # edit subcommand needs at least 2 args
    res = subprocess.run([bin_path, "edit"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Usage:" in res.stdout

def test_backlog_list_subcommand():
    """Verifies bin/backlog list executes successfully and outputs backlog items."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/backlog')
    assert os.path.exists(bin_path)
    
    res = subprocess.run([bin_path, "list"], capture_output=True, text=True, check=True)
    assert res.returncode == 0
    assert "Backlog" in res.stdout or "empty" in res.stdout

