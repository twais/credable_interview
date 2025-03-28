import os
import pysftp


class SFTPIngest:
    """
    Handles the ingestion of data from a specified SFTP location.
    This class connects to an SFTP server, retrieves files, and processes them as needed.
    """

    def __init__(self, sftp_host, sftp_user, sftp_pass):
        with pysftp.Connection(
            sftp_host, username=sftp_user, password=sftp_pass
        ) as sftp:
            self.sftp = sftp

    def get_files(self, remote_dir, local_dir):
        """
        Retrieves files from the SFTP server and saves them to the local directory. Retrieves only CSV files.
        :param remote_dir: The directory on the SFTP server to retrieve files from.
        :param local_dir: The local directory to save the files to.
        """

        try:
            # Check if the local directory exists, if not create it
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            # Get only csv files
            file_list = self.sftp.listdir(remote_dir)
            file_list = [f for f in file_list if f.endswith(".csv")]
            # Retrieve files
            for file in file_list:
                remote_file = os.path.join(remote_dir, file)
                local_file = os.path.join(local_dir, file)
                self.sftp.get(remote_file, local_file)
            return file_list
        except FileNotFoundError as e:
            # Handle file not found error
            print(f"Error: {e}")
        except Exception as ex:
            # Handle other exceptions
            print(f"Error: {ex}")
