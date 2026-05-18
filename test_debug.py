import sys
import os

from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath("."))
from orchestrator.flow_state_manager import sync_and_clean_node

@patch('orchestrator.flow_state_manager.github_client.get_open_prs', return_value=[])
@patch('orchestrator.flow_state_manager.github_client.list_issues_by_label', return_value=[])
@patch('orchestrator.flow_state_manager.subprocess.run')
@patch('orchestrator.node_lifecycle.subprocess.run')
def test_sync_and_clean_node(mock_node_run, mock_run, mock_list, mock_get_open_prs):
    mock_result = MagicMock()
    mock_result.stdout = "  main\n* node/1-test\n  old-branch\n"
    mock_run.return_value = mock_result
    
    sync_and_clean_node()
    print("MOCK RUN:", mock_run.call_args_list)
    print("MOCK NODE RUN:", mock_node_run.call_args_list)

test_sync_and_clean_node()
