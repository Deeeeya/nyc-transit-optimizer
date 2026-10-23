import pandas as pd # 'as pd' part gives pandas a nickname, so you write 'pd.' instead of 'pandas.' everywhere
from database import get_connection

conn = get_connection() # This calls your function from database.py, and the connection it returns gets stored in conn.
print("Connected to Supabase!") # always keep messages in the intended file, the database function stays quiet

df = pd.read_csv("data/gtfs_subway/stops.txt", dtype=str) # reads the file and gives back a DataFrame. df is the conventional variable name for one. dtype=str means “read everything as text.” You’ll convert the coordinates and location_type back to numbers yourself later, on purpose. Explicit beats implicit.
print(df.head()) # df.head() shows the first 5 rows. it's the quickest way to check that the data has loaded correctly

conn.close() # This hangs up the connection. It goes at the very end, because tomorrow’s insert code will go between opening and closing. The pattern is:
