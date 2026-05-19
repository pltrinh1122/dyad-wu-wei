import os
import tempfile
import yaml
import pytest
from unittest import mock
from orchestrator.node_lifecycle import load_node_status_config, load_node_classification_config, BaseNode

def test_load_node_status_config_success():
    mock_yaml_content = {
        "node_attributes": {
            "status": {
                "in_progress": "status: in-progress"
            },
            "classification": {
                "backlog": "backlog"
            }
        }
    }
    with mock.patch("os.path.exists", return_value=True):
        with mock.patch("builtins.open", mock.mock_open(read_data=yaml.dump(mock_yaml_content))):
            status_config = load_node_status_config()
            assert status_config.get("in_progress") == "status: in-progress"

            class_config = load_node_classification_config()
            assert class_config.get("backlog") == "backlog"

def test_load_node_status_config_not_found():
    with mock.patch("os.path.exists", return_value=False):
        status_config = load_node_status_config()
        assert status_config == {}

        class_config = load_node_classification_config()
        assert class_config == {}

@mock.patch("orchestrator.node_lifecycle.load_node_status_config")
@mock.patch("orchestrator.node_lifecycle.github_client.add_label")
def test_base_node_set_status(mock_add_label, mock_load_config):
    mock_load_config.return_value = {"in_progress": "status: in-progress"}
    node = BaseNode("100")
    node.set_status("in_progress")
    mock_add_label.assert_called_once_with("100", "status: in-progress")

@mock.patch("orchestrator.node_lifecycle.load_node_status_config")
def test_base_node_set_status_invalid(mock_load_config):
    mock_load_config.return_value = {"in_progress": "status: in-progress"}
    node = BaseNode("100")
    with pytest.raises(ValueError, match="Status key 'invalid' is not defined in node.yml"):
        node.set_status("invalid")

@mock.patch("orchestrator.node_lifecycle.load_node_classification_config")
@mock.patch("orchestrator.node_lifecycle.github_client.add_label")
def test_base_node_set_classification(mock_add_label, mock_load_config):
    mock_load_config.return_value = {"backlog": "backlog"}
    node = BaseNode("100")
    node.set_classification("backlog")
    mock_add_label.assert_called_once_with("100", "backlog")

@mock.patch("orchestrator.node_lifecycle.load_node_classification_config")
def test_base_node_set_classification_invalid(mock_load_config):
    mock_load_config.return_value = {"backlog": "backlog"}
    node = BaseNode("100")
    with pytest.raises(ValueError, match="Classification key 'invalid' is not defined in node.yml"):
        node.set_classification("invalid")
