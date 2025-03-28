# Credable Interview Assessment

## Getting Started 

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Important notes
- For the purposes of this assessment, I am using a public and trial [SFTP server](https://sftpcloud.io/tools/free-sftp-server). Trial expires in 7 days

- SFTP credentials are available on the installing and running on your dev environment section and should be exported as environment variables. (Ideally, these should be shared securely)

- The data used for this assessment is Common Vulnerability Exposure (CVE) data, the data might not be accurate, but follows the format intended for this purpose. Below is a sample head of the file consiting of duplicates and blank lines as well:
```
CVE Number,Description,Discovery Date
CVE-2013-98377,Vulnerability in ABC software allows cross-site scripting.,2018-02-25
CVE-2025-24009,Vulnerability in PQR software allows SQL injection.,2020-09-10

CVE-2024-63917,Vulnerability in MNO software allows denial of service.,2019-04-10
CVE-2014-8359,Vulnerability in MNO software allows SQL injection.,2016-03-26

CVE-2005-69506,Vulnerability in ABC software allows denial of service.,2013-07-02
CVE-2005-69506,Vulnerability in ABC software allows denial of service.,2013-07-02


CVE-2019-8977,Vulnerability in JKL software allows denial of service.,2015-12-12
CVE-2016-75177,Vulnerability in PQR software allows denial of service.,2013-07-12
CVE-2005-69506,Vulnerability in ABC software allows denial of service.,2013-07-02
CVE-2013-16985,Vulnerability in DEF software allows denial of service.,2010-09-20
```

### Prerequisites
Ensure that you have the following installed on your local machine

```
python 3.x
```

### Installing and running on your dev environment

A step by step series of how to get a development env running

The steps are as follows

Create and activate a virtual environment: 
```
virtualenv credable
source credable/bin/activate
```

Clone project, install dependencies and export required environment variables
```
clone https://github.com/twais/credable_interview.git the git repo 
cd into the parent directory (credable_interview)
pip install -r tasks/requirements.txt
export SFTP_USERNAME=credable_test
export SFTP_HOST=us-east-1.sftpcloud.io
export SFTP_PASSWORD=yzxc6YiQVRph8oCzAY1bimHx0fRAb7Jz
```

Run the pipeline:
```
python pipeline.py cve_large_list.csv
```

On a separate command line, run the API:
```
uvicorn tasks.api:app --reload
```

You can now access the service via http://127.0.0.1:8000/, i.e.
- To get all data: http://127.0.0.1:8000/data
- To get CVE data by discovery date: http://127.0.0.1:8000/data?discovery_date=2023-10-02
- To get CVE data by cursor and limits: http://127.0.0.1:8000/data?discovery_date=2023-10-02&cursor=0&limit=10

## Running the tests

pytest -v

### Documentation

The API documentation is available on swagger
```
http://127.0.0.1:8000/docs
```

## Built With
* [Python](https://www.python.org/) - The programming language
* [Fast API](https://pypi.org/project/Flask/) - The web framework used
* [Pytest](https://docs.pytest.org/en/stable/) - The test framework
