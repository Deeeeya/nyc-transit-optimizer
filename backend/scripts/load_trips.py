import pandas as pd
from scripts.loader_utils import bulk_insert

INSERT_SQL = """
    INSERT INTO trips (trip_id, route_id, service_id, trip_headsign, direction_id)
    VALUES %s
    ON CONFLICT (trip_id) DO NOTHING
"""

df = pd.read_csv("data/gtfs_subway/trips.txt", dtype=str)

rows = []
for _, row in df.iterrows():
    rows.append((
        row["trip_id"],
        row["route_id"],
        row["service_id"],
        row["trip_headsign"],
        int(row["direction_id"]),
    ))

bulk_insert(INSERT_SQL, rows, "trips")