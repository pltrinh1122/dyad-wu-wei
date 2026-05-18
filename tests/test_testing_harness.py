import os
import pytest
from unittest.mock import patch, MagicMock
from skills.testing_harness import run_tests

@patch('skills.testing_harness.subprocess.run')
def test_run_tests(mock_run):
    mock_result = MagicMock()
    mock_result.stdout = "============================= test session starts ==============================\n3 passed in 0.01s"
    mock_result.returncode = 0
    mock_run.return_value = mock_result
    
    # We mock os.environ so we have a predictable base environment
    with patch.dict(os.environ, {"PATH": "/usr/bin"}, clear=True):
        exit_code = run_tests("tests/test_dummy.py")
        
    assert exit_code == 0
    mock_run.assert_called_once()
    
    # Check the subprocess arguments
    call_args = mock_run.call_args
    args = call_args[0][0]
    kwargs = call_args[1]
    
    assert args[0].endswith("pytest")
    assert args[1] == "tests/test_dummy.py"
    assert "env" in kwargs
    assert kwargs["env"]["PYTHONPATH"] == "."
    assert kwargs["env"]["PATH"] == "/usr/bin" # Ensures base env was copied
