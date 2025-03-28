import argparse
from sftp_ingest import SFTPIngest
from csv_cleanup import CSVCleanup
import os

# Pass the file name to be processed as an argument
parser = argparse.ArgumentParser(
    description="Run the pipeline with a specified file name."
)
parser.add_argument(
    "file_name",
    type=str,
    help="The name of the file to process (e.g., cve_large_list.csv).",
)
args = parser.parse_args()
# check that argument ends with .csv
if not args.file_name.endswith(".csv"):
    raise ValueError("File name must be a .csv")

file_name = args.file_name

sftp_ingest = SFTPIngest(
    os.getenv("SFTP_HOST"), os.getenv("SFTP_USERNAME"), os.getenv("SFTP_PASSWORD")
)
result = sftp_ingest.get_files("credable_files", "credable_files", file_name)
sftp_ingest.close()

cleanup = CSVCleanup(f"credable_files/{file_name}")
cleanup.remove_duplicates()
cleanup.remove_empty_lines()
