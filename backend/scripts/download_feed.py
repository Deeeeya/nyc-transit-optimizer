import os
import zipfile

import requests

FEED_URL = "https://rrgtfsfeeds.s3.amazonaws.com/gtfs_supplemented.zip"
ZIP_PATH = "data/gtfs_subway.zip"
DATA_DIR = "data/gtfs_subway"

REQUIRED_FILES = [
    "stops.txt",
    "routes.txt",
    "trips.txt",
    "calendar.txt",
    "calendar_dates.txt",
    "stop_times.txt",
    "transfers.txt",
    "feed_info.txt",
]


def download_feed():
    print("Downloading feed...") # requests.get(url) sends the request, just like your browser does when you click a link
    response = requests.get(FEED_URL, timeout=120) # timeout=120: give up after 120 seconds instead of waiting forever if the MTA’s server hangs. Always set a timeout on network calls
    response.raise_for_status() # crashes loudly if the server returns an error (like a 404 Not Found). Without it, you might save an error page as your “zip” and only find out later. That’s fail fast again!
    # with automatically closes the file when the block ends, even if an error happens.
    with open(ZIP_PATH, "wb") as file: # "wb" = write, binary. A zip isn’t text, so it’s written as raw bytes
        file.write(response.content) # response.content is the downloaded file, as raw bytes

    size_mb = len(response.content) / 1_000_000
    print(f"Downloaded {size_mb:.1f} MB")
    

def extract_feed():
    with zipfile.ZipFile(ZIP_PATH) as zip_file:
        zip_file.extractall(DATA_DIR) # extractall unzips everything into the folder, and creates the folder if it doesn’t exist. It also overwrites files with the same names, which is exactly what you want for a refresh.

    missing = []
    for name in REQUIRED_FILES:
        if not os.path.exists(os.path.join(DATA_DIR, name)): # Why os.path.join? Windows uses \ in paths, and Mac/Linux use /. join picks the right one automatically.
            missing.append(name)
    
    if missing: # In Python, an empty list counts as False, and a non-empty list counts as True. So this reads naturally as “if anything is missing...”
        raise FileNotFoundError(f"Feed is missing files: {missing}") # raise creates an error on purpose, stopping the script with a clear message. It’s much better than loading a broken feed into your database!

    print(f"Extracted feed into {DATA_DIR}")


def main():
    download_feed()
    extract_feed()


if __name__ == "__main__":
    main()