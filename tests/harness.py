import os
from unittest.mock import MagicMock

class AntigravityTestHarness:
    """Utility class to manage complex test states and mock configurations."""
    
    def __init__(self):
        self.mocks = {}

    def setup_node_state(self, mock_gh, mock_fe, node_id=123, status="Act"):
        """Configures multiple mocks to simulate a specific node state."""
        mock_gh.get_issue_details.return_value = {
            "number": node_id,
            "title": f"Test Node {node_id}",
            "body": "## Goal\nTest Goal",
            "labels": [{"name": f"status: {status}"}]
        }
        mock_fe.read_active_node.return_value = f"Node {node_id}: Test Node {node_id}"
        
    def configure_subprocess_sequences(self, mock_sub, behaviors):
        """Allows configuring a sequence of subprocess behaviors."""
        def side_effect(*args, **kwargs):
            cmd = args[0] if args else kwargs.get("args")
            for pattern, result in behaviors.items():
                if any(pattern in str(c) for c in cmd):
                    if isinstance(result, Exception):
                        raise result
                    return MagicMock(returncode=result.get("code", 0), 
                                     stdout=result.get("stdout", ""),
                                     stderr=result.get("stderr", ""))
            return MagicMock(returncode=0, stdout="")
        
        mock_sub.side_effect = side_effect
