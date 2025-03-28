from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
import os
import csv
from datetime import datetime

app = FastAPI()

DATA_DIR = "credable_files"


@app.get("/data")
def get_data():
    pass
