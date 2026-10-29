from datetime import datetime
import pandas as pd
from scripts.loader_utils import bulk_insert

INSERT_SQL = """
    INSERT INTO calendar (service_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_date, end_date)
    VALUES %s
    ON CONFLICT (service_id) DO NOTHING
"""


def to_bool(value):
    return value == "1" # In Python, == returns a boolean. So comparing the value to "1" gives you exactly what you need. Python’s booleans are capitalized: True and False.


def to_date(value):
    return datetime.strptime(value, "%Y%m%d").date() # strptime means “string parse time”: it turns text into a date. / "%Y%m%d" describes the text’s format: %Y = 4-digit year, %m = month, %d = day. So it reads 2026 / 05 / 26. / .date() keeps just the date part and drops the time.


df = pd.read_csv("data/gtfs_subway/calendar.txt", dtype=str)

rows = []
for _, row in df.iterrows():
    rows.append((
        row["service_id"],
        to_bool(row["monday"]),
        to_bool(row["tuesday"]),
        to_bool(row["wednesday"]),
        to_bool(row["thursday"]),
        to_bool(row["friday"]),
        to_bool(row["saturday"]),
        to_bool(row["sunday"]),
        to_date(row["start_date"]),
        to_date(row["end_date"]),
    ))

bulk_insert(INSERT_SQL, rows, "calendar services")