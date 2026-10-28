import pandas as pd
from scripts.loader_utils import bulk_insert

INSERT_SQL = """
    INSERT INTO routes (route_id, route_short_name, route_long_name, route_type, route_color, route_text_color, route_sort_order)
    VALUES %s
    ON CONFLICT (route_id) DO NOTHING
"""

df = pd.read_csv("data/gtfs_subway/routes.txt", dtype=str)

rows = []
for _, row in df.iterrows():
    rows.append((
        row["route_id"],
        row["route_short_name"],
        row["route_long_name"],
        int(row["route_type"]),
        row["route_color"],
        row["route_text_color"],
        int(row["route_sort_order"]),
    ))

bulk_insert(INSERT_SQL, rows, "routes")