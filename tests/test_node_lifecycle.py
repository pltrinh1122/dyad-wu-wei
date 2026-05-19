import os
import tempfile
import yaml
from unittest import mock
from orchestrator.node_lifecycle import load_node_status_config, load_node_classification_config

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
