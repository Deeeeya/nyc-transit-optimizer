from datetime import datetime
import pandas as pd
from scripts.loader_utils import bulk_insert

INSERT_SQL = """
    INSERT INTO calendar_dates (service_id, service_date, exception_type)
    VALUES %s
    ON CONFLICT (service_id, service_date) DO NOTHING
"""


def to_date(value):
    return datetime.strptime(value, "%Y%m%d").date()


def load():
    df = pd.read_csv("data/gtfs_subway/calendar_dates.txt", dtype=str)

    rows = []
    for _, row in df.iterrows():
        rows.append((
            row["service_id"],
            to_date(row["date"]),
            int(row["exception_type"]),
        ))


    bulk_insert(INSERT_SQL, rows, "calendar dates")


if __name__ == "__main__":
    load()
