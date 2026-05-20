import os
import subprocess
import pytest

# ── Hermetic gh stub ──────────────────────────────────────────────────────────
# Prepend tests/fixtures/ to PATH so the stub gh replaces the real gh CLI for
# every test in this module. Prevents live GitHub API calls in CI.
_FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

@pytest.fixture(autouse=True, scope="module")
def stub_gh_cli():
    """Inject tests/fixtures/ into PATH, activating the hermetic gh stub."""
    original_path = os.environ.get("PATH", "")
    os.environ["PATH"] = _FIXTURES_DIR + os.pathsep + original_path
    yield
    os.environ["PATH"] = original_path

def test_node_test_subcommand():
    """Verifies the bin/node test subcommand executes successfully."""
    if os.environ.get("ANTIGRAVITY_RUNNING_TESTS"):
        return
        
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/node')
    assert os.path.exists(bin_path)
    
    # Run the shell script and verify it executes our pytest suite successfully
    try:
        res = subprocess.run([bin_path, "test"], capture_output=True, text=True, check=True)
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
    assert "usage:" in res.stderr.lower() or "usage:" in res.stdout.lower()

    # Invalid subcommand
    res = subprocess.run([bin_path, "invalid"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "usage:" in res.stderr.lower() or "usage:" in res.stdout.lower()

def test_node_plan_subcommand_usage():
    """Verifies bin/node plan enforces argument counts and prints usage on errors."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/node')
    assert os.path.exists(bin_path)

    # plan subcommand needs at least 2 args
    res = subprocess.run([bin_path, "plan-start"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "usage:" in res.stderr.lower() or "usage:" in res.stdout.lower()

def test_node_reflect_subcommand_usage():
    """Verifies bin/node reflect enforces argument counts and prints usage on errors."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/node')
    assert os.path.exists(bin_path)

    # reflect subcommand needs at least 7 args
    res = subprocess.run([bin_path, "reflect"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "usage:" in res.stderr.lower() or "usage:" in res.stdout.lower()

def test_node_view_subcommand_usage():
    """Verifies bin/node view enforces argument counts and prints usage on errors."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/node')
    assert os.path.exists(bin_path)

    # view subcommand needs at least 1 arg
    res = subprocess.run([bin_path, "view"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "usage:" in res.stderr.lower() or "usage:" in res.stdout.lower()

def test_backlog_wrapper_usage():
    """Verifies bin/backlog prints usage when no arguments or invalid subcommands are passed."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/backlog')
    assert os.path.exists(bin_path)
    
    # No args
    res = subprocess.run([bin_path], capture_output=True, text=True)
    assert res.returncode != 0
    assert "usage:" in res.stderr.lower() or "usage:" in res.stdout.lower()

    # Invalid subcommand
    res = subprocess.run([bin_path, "invalid"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "usage:" in res.stderr.lower() or "usage:" in res.stdout.lower() or "invalid choice" in res.stderr.lower()

def test_backlog_subcommand_usage():
    """Verifies bin/backlog subcommands enforce argument counts and print usage on errors."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/backlog')
    assert os.path.exists(bin_path)

    # new subcommand needs at least 3 args
    res = subprocess.run([bin_path, "new"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "usage:" in res.stderr.lower() or "usage:" in res.stdout.lower()

    # view subcommand needs at least 1 arg
    res = subprocess.run([bin_path, "view"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "usage:" in res.stderr.lower() or "usage:" in res.stdout.lower()

    # edit subcommand needs at least 2 args
    res = subprocess.run([bin_path, "edit"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "usage:" in res.stderr.lower() or "usage:" in res.stdout.lower()

def test_backlog_list_subcommand():
    """Verifies bin/backlog list executes successfully and outputs backlog items."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/backlog')
    assert os.path.exists(bin_path)
    
    res = subprocess.run([bin_path, "list"], capture_output=True, text=True, check=True)
    assert res.returncode == 0
    assert "Backlog" in res.stdout or "empty" in res.stdout

def test_meta_wrapper_usage():
    """Verifies bin/meta prints usage when no arguments or invalid subcommands are passed."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/meta')
    assert os.path.exists(bin_path)
    
    # No args
    res = subprocess.run([bin_path], capture_output=True, text=True)
    assert res.returncode != 0
    assert "usage:" in res.stderr.lower() or "usage:" in res.stdout.lower()

    # Invalid subcommand
    res = subprocess.run([bin_path, "invalid"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "Unknown subcommand:" in res.stdout

def test_meta_link_subcommand_usage():
    """Verifies bin/meta link enforces argument counts and prints usage on errors."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/meta')
    assert os.path.exists(bin_path)

    # link needs at least 2 args
    res = subprocess.run([bin_path, "link"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "usage:" in res.stderr.lower() or "usage:" in res.stdout.lower()

def test_meta_check_subcommand_usage():
    """Verifies bin/meta check enforces argument counts and prints usage on errors."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/meta')
    assert os.path.exists(bin_path)

    # check needs at least 1 arg
    res = subprocess.run([bin_path, "check"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "usage:" in res.stderr.lower() or "usage:" in res.stdout.lower()

def test_meta_active_subcommand_usage():
    """Verifies bin/meta active enforces argument counts and prints usage on errors."""
    bin_path = os.path.join(os.path.dirname(__file__), '../bin/meta')
    assert os.path.exists(bin_path)

    # active needs at least 4 args
    res = subprocess.run([bin_path, "active"], capture_output=True, text=True)
    assert res.returncode != 0
    assert "usage:" in res.stderr.lower() or "usage:" in res.stdout.lower()


