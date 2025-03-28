from fastapi import FastAPI, Query, HTTPException
from typing import Optional
import os
import csv
from datetime import datetime

app = FastAPI()

DATA_DIR = "credable_files"
DATA_SOURCE_NAME = "cve_large_list.csv"


@app.get("/data")
def get_data(
    discovery_date: Optional[str] = Query(
        None, description="CVE discovery date in YYYY-MM-DD format"
    ),
    cursor: Optional[int] = Query(0, description="Cursor for pagination with default value as 0"),
    limit: Optional[int] = Query(
        10, description="Number of CVE records to return with default value as 10"
    ),
):
    """
    Retrieve data from a specified file with optional date-based filtering and cursor-based pagination.
    :param discovery_date: Filter records by when CVE was discovered (YYYY-MM-DD).
    :param cursor: The starting index for pagination.
    :param limit: The number of records to return.
    """
    file_path = os.path.join(DATA_DIR, DATA_SOURCE_NAME)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    cve_data = []
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Filter by discovery_date if provided
                if discovery_date:
                    if "Discovery Date" in row:
                        row_date = datetime.strptime(row["Discovery Date"], "%Y-%m-%d")
                        filter_date = datetime.strptime(discovery_date, "%Y-%m-%d")
                        if row_date != filter_date:
                            continue
                cve_data.append(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {e}")

    # pagination
    paginated_cve_data = cve_data[cursor : cursor + limit]

    return {
        "data": paginated_cve_data,
        "cursor": (
            cursor + len(paginated_cve_data) if len(paginated_cve_data) == limit else None
        ),
    }
