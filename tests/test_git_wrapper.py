import unittest
from unittest import mock
from drivers.git_wrapper import run_git_command

class TestGitWrapper(unittest.TestCase):
    @mock.patch("drivers.git_wrapper.subprocess.run")
    def test_run_git_command(self, mock_run):
        mock_run.return_value = mock.MagicMock(returncode=0)
        ret = run_git_command(["status"])
        mock_run.assert_called_once_with(["git", "status"])
        self.assertEqual(ret, 0)
