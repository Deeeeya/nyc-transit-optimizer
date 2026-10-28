import pandas as pd # 'as pd' part gives pandas a nickname, so you write 'pd.' instead of 'pandas.' everywhere
from scripts.loader_utils import bulk_insert

# triple quotes let a string span multiple lines, the ON CONFLICT line means if a stop already exists, do nothing and skip it
INSERT_SQL = """  
    INSERT INTO stops (stop_id, stop_name, stop_lat, stop_lon, location_type, parent_station)
    VALUES %s
    ON CONFLICT (stop_id) DO NOTHING 
""" # you use PARAMETERIZED QUIERIES --> you write placeholders (%s) in the SQL and hand the values over separately, psycopg2 treats them strictly as data, never as code to prevent malicious SQL injections

# helper functions (defined at the top, used later)
def clean_text(value):
    if pd.isna(value):
        return None
    return value 

def clean_int(value):
    if pd.isna(value):
        return None
    return int(value)

# reads the file and gives back a DataFrame. df is the conventional variable name for one. dtype=str means “read everything as text.” You’ll convert the coordinates and location_type back to numbers yourself later, on purpose. Explicit beats implicit.
df = pd.read_csv("data/gtfs_subway/stops.txt", dtype=str) 

# build a list of clean tuples, one per stop
rows = []
# Each time through, it gives two things: the row number and the row itself. We don’t need the row number, so we catch it with _, which is Python’s convention for “I’m ignoring this.”
for _, row in df.iterrows(): # this function hands you rows one at a time
    rows.append((
        row["stop_id"], # stop id and name don't need cleaning because every stop has both
        row["stop_name"],
        float(row["stop_lat"]),
        float(row["stop_lon"]),
        clean_int(row["location_type"]), # if the cell is empty, it returns None; otherwise it converts the value to a whole number.
        clean_text(row["parent_station"]) # if the cell is empty, it returns None; otherwise it returns the value unchanged.
    ))

# split into stations (no parent) and platforms (have a parent)
stations = []
platforms = []
for row in rows:
    if row[5] is None:
        stations.append(row)
    else:
        platforms.append(row)

# stations first, so platforms' parents already exist
ordered_rows = stations + platforms # partitioning

bulk_insert(INSERT_SQL, rows, "stops")