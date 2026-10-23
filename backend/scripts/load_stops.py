import pandas as pd # 'as pd' part gives pandas a nickname, so you write 'pd.' instead of 'pandas.' everywhere
from psycopg2.extras import execute_values
from database import get_connection

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

# This calls your function from database.py, and the connection it returns gets stored in conn.
conn = get_connection() # the open phone line to Supabase.
print("Connected to Supabase!")
cur = conn.cursor() # curr (the cursor) is what actually speaks SQL over that line. You send queries through it.
 
try: # attempt the work
    execute_values(cur, INSERT_SQL, ordered_rows) # With this, your SQL has one single %s after VALUES, and it fills in all the rows for you.
    conn.commit()
    print(f"Loaded {len(ordered_rows)} stops (existing ones skipped)") # The f before the quotes lets you put variables inside { }. It’s the same as JS template literals: `Loaded ${count} stops`.
except Exception: # something broke → undo it
    conn.rollback() # if something breaks halfway, it cancels everything, so you never end up with half a table
    print("Something went wrong, rolled back. Nothing was saved.")
    raise # re-shows the original error after rolling back, so you can still see what went wrong.
finally: # ALWAYS runs, success or failure → clean up
    cur.close()
    conn.close()