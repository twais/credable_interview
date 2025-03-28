import os
import pysftp


class SFTPIngest:
    """
    Handles the ingestion of data from a specified SFTP location.
    This class connects to an SFTP server, retrieves files, and processes them as needed.
    """

    def __init__(self, sftp_host, sftp_user, sftp_pass):
        try:
            # Establish SFTP connection
            self.sftp = pysftp.Connection(
                sftp_host, username=sftp_user, password=sftp_pass
            )
        except Exception as e:
            print(f"Failed to connect to SFTP server: {e}")
            self.sftp = None

    def get_files(self, remote_dir, local_dir, file_name):
        """
        Retrieves files from the SFTP server and saves them to the local directory. Retrieves only CSV files.
        :param remote_dir: The directory on the SFTP server to retrieve files from.
        :param local_dir: The local directory to save the files to.
        """

        try:
            # Create local directory if not exists
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            # Get only csv file with specified name
            self.sftp.get(f"{remote_dir}/{file_name}", f"{local_dir}/{file_name}")
            return True

        except FileNotFoundError as e:
            # Handle file not found error
            print(f"Error: {e}")
        except Exception as ex:
            # Handle other exceptions
            print(f"Error: {ex}")

    def close(self):
        """Closes the SFTP connection."""
        if self.sftp:
            self.sftp.close()
            self.sftp = None
