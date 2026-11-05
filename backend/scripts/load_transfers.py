import pandas as pd
from scripts.loader_utils import bulk_insert

INSERT_SQL = """
    INSERT INTO transfers (from_stop_id, to_stop_id, transfer_type, min_transfer_time)
    VALUES %s
    ON CONFLICT (from_stop_id, to_stop_id) DO NOTHING
"""


def load():
    df = pd.read_csv("data/gtfs_subway/transfers.txt", dtype=str)

    rows = []
    for _, row in df.iterrows():
        rows.append((
            row["from_stop_id"],
            row["to_stop_id"],
            int(row["transfer_type"]),
            int(row["min_transfer_time"]),
        ))

    bulk_insert(INSERT_SQL, rows, "transfers")


if __name__ == "__main__":
    load()