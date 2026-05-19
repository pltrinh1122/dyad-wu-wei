import pytest
import os
from unittest.mock import patch, mock_open
from skills.issue_factory import render_template

def test_render_template_success():
    mock_template = "Hello {name}, your score is {score}."
    
    with patch("builtins.open", mock_open(read_data=mock_template)):
        with patch("os.path.exists", return_value=True):
            result = render_template("test_template", {"name": "Alice", "score": 100})
            assert result == "Hello Alice, your score is 100."

def test_render_template_missing_key():
    mock_template = "Hello {name}, your score is {score}."
    
    with patch("builtins.open", mock_open(read_data=mock_template)):
        with patch("os.path.exists", return_value=True):
            with pytest.raises(KeyError):
                render_template("test_template", {"name": "Alice"})

def test_render_template_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            render_template("non_existent", {})

def test_render_nba_banner():
    # Use real template file for a smoke test if it exists, 
    # or mock it to verify the key mapping.
    kwargs = {
        "mode_label": "Test Mode",
        "path_info": "Path 1: Title",
        "recommendations_list": "  → #2: Rec"
    }
    # We verify that it doesn't raise KeyError
    result = render_template("nba_banner", kwargs)
    assert "Test Mode" in result
    assert "Path 1: Title" in result
    assert "#2: Rec" in result
