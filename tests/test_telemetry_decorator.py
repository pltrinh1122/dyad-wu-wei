import unittest
import os
import json
import uuid
from unittest.mock import patch, MagicMock
from kernel.daemon_telemetry import TelemetryManager, record_execution

class TestTelemetryDecorator(unittest.TestCase):
    def setUp(self):
        os.environ["SPAO_TELEMETRY_NO_TEST_SAFETY"] = "1"
        self.test_ledger = "test_telemetry.jsonl"
        if os.path.exists(self.test_ledger):
            os.remove(self.test_ledger)
        self.manager = TelemetryManager(ledger_path=self.test_ledger)

    def tearDown(self):
        if os.path.exists(self.test_ledger):
            os.remove(self.test_ledger)

    def test_record_execution_success(self):
        @record_execution(stage="test_stage")
        def sample_func(arg1):
            return f"hello {arg1}"

        with patch('kernel.daemon_telemetry.TelemetryManager._get_default_ledger_path', return_value=self.test_ledger):
            result = sample_func("world")
            
        self.assertEqual(result, "hello world")
        
        with open(self.test_ledger, "r") as f:
            lines = f.readlines()
            
        self.assertEqual(len(lines), 2)
        start_event = json.loads(lines[0])
        finish_event = json.loads(lines[1])
        
        self.assertEqual(start_event["event"], "START")
        self.assertEqual(start_event["stage"], "TEST_STAGE")
        self.assertIn(start_event["domain"], ["__main__", "tests"])
        
        self.assertEqual(finish_event["event"], "FINISH")
        self.assertEqual(finish_event["metadata"]["status"], "success")
        self.assertEqual(start_event["execution_id"], finish_event["execution_id"])

    def test_record_execution_error(self):
        @record_execution(stage="error_stage")
        def failing_func():
            raise ValueError("boom")

        with patch('kernel.daemon_telemetry.TelemetryManager._get_default_ledger_path', return_value=self.test_ledger):
            with self.assertRaises(ValueError):
                failing_func()
                
        with open(self.test_ledger, "r") as f:
            lines = f.readlines()
            
        self.assertEqual(len(lines), 2)
        finish_event = json.loads(lines[1])
        self.assertEqual(finish_event["metadata"]["status"], "error")
        self.assertEqual(finish_event["metadata"]["error"], "boom")

    def test_node_id_extraction(self):
        class MockNode:
            def __init__(self, issue_id):
                self.issue_id = issue_id
            
            @record_execution(stage="node_stage")
            def do_work(self):
                pass

        node = MockNode("123")
        with patch('kernel.daemon_telemetry.TelemetryManager._get_default_ledger_path', return_value=self.test_ledger):
            node.do_work()
            
        with open(self.test_ledger, "r") as f:
            lines = f.readlines()
            
        start_event = json.loads(lines[0])
        self.assertEqual(start_event["node_id"], "123")

if __name__ == "__main__":
    unittest.main()
