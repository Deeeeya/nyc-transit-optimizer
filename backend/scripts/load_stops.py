import pandas as pd # 'as pd' part gives pandas a nickname, so you write 'pd.' instead of 'pandas.' everywhere

df = pd.read_csv("data/gtfs_subway/stops.txt", dtype=str) # reads the file and gives back a DataFrame. df is the conventional variable name for one. dtype=str means “read everything as text.” You’ll convert the coordinates and location_type back to numbers yourself later, on purpose. Explicit beats implicit.
print(df.head()) # df.head() shows the first 5 rows. it's the quickest way to check that the data has loaded correctly
