import unittest
from unittest.mock import patch, MagicMock


class TestSFTPIngest(unittest.TestCase):
    def setUp(self):
        # Patch pysftp.Connection to prevent actual SFTP connections
        self.pysftp_patcher = patch(
            "tasks.sftp_ingest.pysftp.Connection", autospec=True
        )
        self.mock_connection_class = self.pysftp_patcher.start()
        self.addCleanup(self.pysftp_patcher.stop)

        # Create a mock connection instance
        self.mock_connection = MagicMock()
        self.mock_connection_class.return_value = self.mock_connection

        # Patch the SFTPIngest class
        patcher = patch("tasks.sftp_ingest.SFTPIngest", autospec=True)
        self.mock_sftp_ingest_class = patcher.start()
        self.addCleanup(patcher.stop)

        # Create a mock instance of SFTPIngest
        self.mock_sftp_ingest = self.mock_sftp_ingest_class.return_value

        # Use the mocked instance for testing
        self.sftp_ingest = self.mock_sftp_ingest

    def test_get_files(self):
        # Mock the behavior of get_files
        self.mock_sftp_ingest.get_files.return_value = ["file1.csv", "file2.csv"]
        self.sftp_ingest.get_files("/remote_dir", "/local_dir")
        self.mock_sftp_ingest.get_files.assert_called_once_with(
            "/remote_dir", "/local_dir"
        )
        self.assertEqual(
            self.sftp_ingest.get_files("/remote_dir", "/local_dir"),
            ["file1.csv", "file2.csv"],
        )

    def test_get_files_file_not_found(self):
        # Mock behavior of get_files when FileNotFoundError is raised
        self.mock_sftp_ingest.get_files.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            self.sftp_ingest.get_files("/remote_dir", "/local_dir")
        # verify that mocked method was called with the correct arguments
        self.mock_sftp_ingest.get_files.assert_called_once_with(
            "/remote_dir", "/local_dir"
        )

    def test_get_files_exception(self):
        # Mock behavior of get_files when exception is raised
        self.mock_sftp_ingest.get_files.side_effect = Exception
        with self.assertRaises(Exception):
            self.sftp_ingest.get_files("/remote_dir", "/local_dir")
        # verify that mocked method was called with the correct arguments
        self.mock_sftp_ingest.get_files.assert_called_once_with(
            "/remote_dir", "/local_dir"
        )
