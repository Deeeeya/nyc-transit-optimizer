import hashlib
import os

import pandas as pd

from database import get_connection
from scripts import download_feed, load_all
from scripts.download_feed import DATA_DIR # reuses the folder path instead of typing it again (DRY!)

DATA_FILES = [
    "stops.txt",
    "routes.txt",
    "trips.txt",
    "calendar.txt",
    "calendar_dates.txt",
    "stop_times.txt",
    "transfers.txt",
]

BLOCK_SIZE = 1_000_000


def fingerprint_feed(): # Make the fingerprint
    sha = hashlib.sha256() # sha256 is the hashing method: the industry standard

    for name in DATA_FILES:
        with open(os.path.join(DATA_DIR, name), "rb") as file: # "rb" = read, binary
            while True:
                block = file.read(BLOCK_SIZE) # grab the next 1 MB, Memory use stays at 1 MB, no matter how big the file is
                if not block: # empty = end of file
                    break # exit the loop
                sha.update(block) # update(...) feeds data in. You can call it many times, and it all adds up into one fingerprint

    return sha.hexdigest() # hexdigest() gives you the final fingerprint as text → "2cf24dba5fb0a30e..." (64 characters)


def read_feed_version(): # Read the human-readable label from feed_info.txt
    df = pd.read_csv(os.path.join(DATA_DIR, "feed_info.txt"), dtype=str)
    return df["feed_version"].iloc[0] # means “the first row.” feed_info.txt has just one row of data


def get_last_fingerprint(): # Look up the most recent note in the notebook
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT fingerprint FROM feed_metadata ORDER BY loaded_at DESC LIMIT 1") # ORDER BY loaded_at DESC: newest first (DESC = descending) // LIMIT 1: just the top row, which is the most recent load
        row = cur.fetchone() # gives you that row as a tuple, like ("a1b2...",), or None if the table is empty (the very first run!)
    finally:
        cur.close()
        conn.close()
    
    if row is None:
        return None
    return row[0]


def record_load(fingerprint, feed_version): # Write a new note in the notebook
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO feed_metadata (fingerprint, feed_version) VALUES (%s, %s)", # The INSERT uses %s placeholders. Values from outside your code always get parameterized 🔒
            (fingerprint, feed_version),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def main():
    download_feed.main()

    fingerprint = fingerprint_feed()
    last_fingerprint = get_last_fingerprint()

    if fingerprint == last_fingerprint:
        print("Feed unchanged since last load. Skipping reload.")
        return
    
    print("Feed changed. Reloading...")
    load_all.main()
    record_load(fingerprint, read_feed_version())
    print(f"Recorded load: {fingerprint[:12]}...") # shows just the first 12 characters, so the message stays readable


if __name__ == "__main__":
    main()