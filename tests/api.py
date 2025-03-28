import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, mock_open
from datetime import datetime
from tasks.api import app

MOCK_CSV_DATA = """CVE Number,Description,Discovery Date
CVE-2013-98377,Vulnerability in ABC software allows cross-site scripting.,2018-02-25
CVE-2025-24009,Vulnerability in PQR software allows SQL injection.,2020-09-10
CVE-2024-63917,Vulnerability in MNO software allows denial of service.,2019-04-10
CVE-2014-8359,Vulnerability in MNO software allows SQL injection.,2016-03-26
"""

class TestApi(unittest.TestCase):
    def setUp(self):
        # test client for FastAPI app
        self.client = TestClient(app)

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_file_not_found(self, mock_open_file, mock_path_exists):
        mock_path_exists.return_value = False
        response = self.client.get("/data")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "File not found"})

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data=MOCK_CSV_DATA)
    def test_retrieve_all_data(self, mock_open_file, mock_path_exists):
        mock_path_exists.return_value = True
        response = self.client.get("/data")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 4)

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data=MOCK_CSV_DATA)
    def test_filter_by_date(self, mock_open_file, mock_path_exists):
        mock_path_exists.return_value = True
        response = self.client.get("/data?discovery_date=2020-09-10")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 1)
        self.assertEqual(response.json()["data"][0]["Description"], "Vulnerability in PQR software allows SQL injection.")

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data=MOCK_CSV_DATA)
    def test_pagination(self, mock_open_file, mock_path_exists):
        mock_path_exists.return_value = True
        response = self.client.get("/data?cursor=0&limit=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 2)
        self.assertEqual(response.json()["data"][0]["Description"], "Vulnerability in ABC software allows cross-site scripting.")
        self.assertEqual(response.json()["data"][1]["Description"], "Vulnerability in PQR software allows SQL injection.")

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data=MOCK_CSV_DATA)
    def test_date_filter_and_pagination(self, mock_open_file, mock_path_exists):
        mock_path_exists.return_value = True
        response = self.client.get("/data?discovery_date=2019-04-10&cursor=0&limit=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 1)
        self.assertEqual(response.json()["data"][0]["Description"], "Vulnerability in MNO software allows denial of service.")
