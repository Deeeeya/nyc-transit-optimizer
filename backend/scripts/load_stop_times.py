import pandas as pd
from scripts.loader_utils import bulk_insert

INSERT_SQL = """
    INSERT INTO stop_times (trip_id, stop_sequence, stop_id, arrival_seconds, departure_seconds)
    VALUES %s
    ON CONFLICT (trip_id, stop_sequence) DO NOTHING
"""

CHUNK_SIZE = 100_000


def to_seconds(time_text):
    hours, minutes, seconds = time_text.split(":") # .split(":") cuts the text at every colon and gives you a list.
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) # do the math to convert it into seconds

# Instead of loading all 2.5 million rows into memory at once: chunksize makes pandas hand you the file 100,000 rows at a time, as a series of smaller DataFrames. You process one, throw it away, and grab the next. Memory stays small no matter how big the file is.
chunks = pd.read_csv("data/gtfs_subway/stop_times.txt", dtype=str, chunksize=CHUNK_SIZE) 

for chunk_number, chunk in enumerate(chunks, start=1): # enumerate hands you a counter alongside each item. We’ll use it to print “Chunk 1,” “Chunk 2”... so you can watch the progress.
    rows = []
    for trip_id, stop_sequence, stop_id, arrival, departure in zip( # iterrows is fine for small files, but it’s slow: on 2.5 million rows, it’d take ages. zip walks through several columns side by side, and it’s much faster:
        chunk["trip_id"],
        chunk["stop_sequence"],
        chunk["stop_id"],
        chunk["arrival_time"],
        chunk["departure_time"],
    ):
        rows.append((
            trip_id,
            int(stop_sequence),
            stop_id,
            to_seconds(arrival),
            to_seconds(departure),
        ))

    print(f"Chunk {chunk_number}")
    bulk_insert(INSERT_SQL, rows, "stop times", page_size=5000)