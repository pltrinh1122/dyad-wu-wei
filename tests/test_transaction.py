import os
import tempfile
import pytest
from unittest.mock import MagicMock
from kernel.daemon_transaction import FlowTransaction

def test_transaction_success():
    with tempfile.TemporaryDirectory() as tmp_dir:
        md_file = os.path.join(tmp_dir, "frontier_state.md")
        yml_file = os.path.join(tmp_dir, "frontier_state.yml")
        
        with open(md_file, "w") as f:
            f.write("original md")
        with open(yml_file, "w") as f:
            f.write("original yml")
            
        rollback_mock = MagicMock()
        
        with FlowTransaction(md_file) as tx:
            tx.register_rollback(rollback_mock, "rolled back")
            # Mutate files during transaction
            with open(md_file, "w") as f:
                f.write("mutated md")
            with open(yml_file, "w") as f:
                f.write("mutated yml")
                
        # On success, mutations persist, rollback is NOT called
        with open(md_file, "r") as f:
            assert f.read() == "mutated md"
        with open(yml_file, "r") as f:
            assert f.read() == "mutated yml"
            
        rollback_mock.assert_not_called()

def test_transaction_failure_rollback():
    with tempfile.TemporaryDirectory() as tmp_dir:
        md_file = os.path.join(tmp_dir, "frontier_state.md")
        yml_file = os.path.join(tmp_dir, "frontier_state.yml")
        
        with open(md_file, "w") as f:
            f.write("original md")
        with open(yml_file, "w") as f:
            f.write("original yml")
            
        calls = []
        def rollback_1(val):
            calls.append(val)
        def rollback_2(val):
            calls.append(val)
        
        try:
            with FlowTransaction(md_file) as tx:
                tx.register_rollback(rollback_1, "first")
                tx.register_rollback(rollback_2, "second")
                
                # Mutate files during transaction
                with open(md_file, "w") as f:
                    f.write("mutated md")
                with open(yml_file, "w") as f:
                    f.write("mutated yml")
                    
                raise ValueError("Simulated failure")
        except ValueError:
            pass
            
        # On failure, files should be restored to original contents
        with open(md_file, "r") as f:
            assert f.read() == "original md"
        with open(yml_file, "r") as f:
            assert f.read() == "original yml"
            
        # Rollbacks should be called in REVERSE order
        assert calls == ["second", "first"]

