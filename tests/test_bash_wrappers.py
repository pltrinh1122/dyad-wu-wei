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

def test_plan_node_wrapper_usage():
    """Verifies bin/plan-node prints usage when insufficient arguments are passed."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/plan-node')
    assert os.path.exists(bin_path)
    
    res = subprocess.run([bin_path], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Usage:" in res.stdout

def test_reflect_node_wrapper_usage():
    """Verifies bin/reflect-node prints usage when insufficient arguments are passed."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/reflect-node')
    assert os.path.exists(bin_path)
    
    res = subprocess.run([bin_path], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Usage:" in res.stdout

def test_backlog_new_wrapper_usage():
    """Verifies bin/backlog-new prints usage when insufficient arguments are passed."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/backlog-new')
    assert os.path.exists(bin_path)
    
    res = subprocess.run([bin_path], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Usage:" in res.stdout

def test_backlog_edit_wrapper_usage():
    """Verifies bin/backlog-edit prints usage when insufficient arguments are passed."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/backlog-edit')
    assert os.path.exists(bin_path)
    
    res = subprocess.run([bin_path], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Usage:" in res.stdout

def test_backlog_view_wrapper_usage():
    """Verifies bin/backlog-view prints usage when insufficient arguments are passed."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/backlog-view')
    assert os.path.exists(bin_path)
    
    res = subprocess.run([bin_path], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Usage:" in res.stdout

def test_backlog_list_wrapper():
    """Verifies bin/backlog-list executes successfully and lists backlog items."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/backlog-list')
    assert os.path.exists(bin_path)
    
    res = subprocess.run([bin_path], capture_output=True, text=True, check=True)
    assert res.returncode == 0
    assert "Backlog" in res.stdout or "empty" in res.stdout

