import unittest
from tasks.csv_cleanup import CSVCleanup
import os
import csv


class TestCSVCleanup(unittest.TestCase):
    def setUp(self):
        self.file_path = "tests/cve.csv"
        self.cleanup = CSVCleanup(self.file_path)

    def test_remove_duplicates(self):
        with open(self.file_path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["cve-2018-0001"])
            writer.writerow(["cve-2018-0002"])
            writer.writerow(["cve-2018-0001"])
        self.cleanup.remove_duplicates()
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        self.assertEqual(lines, ["cve-2018-0001\n", "cve-2018-0002\n"])

    def test_remove_empty_lines(self):
        with open(self.file_path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["cve-2018-0001"])
            writer.writerow([""])
            writer.writerow(["cve-2018-0002"])
        self.cleanup.remove_empty_lines()
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        self.assertEqual(lines, ["cve-2018-0001\n", "cve-2018-0002\n"])

    def tearDown(self):
        # remove test file
        os.remove(self.file_path)
