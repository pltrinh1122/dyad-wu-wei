import pytest
from unittest.mock import patch, MagicMock
from kernel.node_lifecycle import TerminalNode
from kernel.daemon_node import abort_node

@patch("kernel.node_lifecycle.TerminalNode.set_classification")
@patch("kernel.node_lifecycle.TerminalNode.set_status")
@patch("kernel.node_lifecycle.git_client")
@patch("kernel.node_lifecycle.agent_frontier")
@patch("kernel.node_lifecycle.FlowTransaction")
@patch("drivers.path_resolver.resolve_workspace_path")
def test_abort_node_flow(mock_resolve_workspace_path, mock_tx, mock_frontier, mock_git, mock_set_status, mock_set_classification):
    mock_resolve_workspace_path.return_value = "/dummy/frontier.md"
    mock_tx.return_value.__enter__.return_value = MagicMock()
    
    node = TerminalNode("123")
    node.abort("artifacts/frontier_state.md")
    
    mock_set_status.assert_called_with("todo")
    mock_set_classification.assert_called_with("backlog")
