import unittest
import subprocess
import os
import tempfile
import stat

class TestShellHooks(unittest.TestCase):
    def setUp(self):
        self.repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.hooks_script = os.path.join(self.repo_root, "bin", "dyad-shell-hooks.sh")

    def test_agy_dyad(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.makedirs(os.path.join(tmpdir, "bin"))
            status_path = os.path.join(tmpdir, "bin", "status")
            with open(status_path, "w") as f:
                f.write("#!/bin/bash\necho 'STATUS_MOCK_TRIGGERED'\n")
            os.chmod(status_path, stat.S_IRWXU)

            agy_mock_path = os.path.join(tmpdir, "bin", "agy")
            with open(agy_mock_path, "w") as f:
                f.write("#!/bin/bash\necho 'AGY_MOCK_TRIGGERED'\n")
            os.chmod(agy_mock_path, stat.S_IRWXU)

            script = f"""
            export PATH="{os.path.join(tmpdir, 'bin')}:$PATH"
            source {self.hooks_script}
            cd {tmpdir}
            agy_dyad arg1 arg2
            """
            
            result = subprocess.run(["bash", "-c", script], capture_output=True, text=True)
            self.assertIn("AGY_MOCK_TRIGGERED", result.stdout)
            self.assertIn("STATUS_MOCK_TRIGGERED", result.stdout)

    def test_claude_dyad(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.makedirs(os.path.join(tmpdir, "bin"))
            status_path = os.path.join(tmpdir, "bin", "status")
            with open(status_path, "w") as f:
                f.write("#!/bin/bash\necho 'STATUS_MOCK_TRIGGERED'\n")
            os.chmod(status_path, stat.S_IRWXU)

            claude_mock_path = os.path.join(tmpdir, "bin", "claude")
            with open(claude_mock_path, "w") as f:
                f.write("#!/bin/bash\necho 'CLAUDE_MOCK_TRIGGERED'\n")
            os.chmod(claude_mock_path, stat.S_IRWXU)

            script = f"""
            export PATH="{os.path.join(tmpdir, 'bin')}:$PATH"
            source {self.hooks_script}
            cd {tmpdir}
            claude_dyad
            """
            
            result = subprocess.run(["bash", "-c", script], capture_output=True, text=True)
            self.assertIn("CLAUDE_MOCK_TRIGGERED", result.stdout)
            self.assertIn("STATUS_MOCK_TRIGGERED", result.stdout)

if __name__ == '__main__':
    unittest.main()
