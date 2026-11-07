import time

from database import get_connection
from scripts import (
    load_stops,
    load_routes,
    load_trips,
    load_calendar,
    load_calendar_dates,
    load_stop_times,
    load_transfers,
)
# TRUNCATE_SQL is a plain constant: there are no user values in it, so there’s nothing to parameterize. (No f-strings in SQL, ever! 🔒)
TRUNCATE_SQL = """
    TRUNCATE stops, routes, trips, calendar, calendar_dates, stop_times, transfers 
"""

# Parents before children, so foreign keys are always satisfied
LOADERS = [
    load_stops,
    load_routes,
    load_trips,
    load_calendar,
    load_calendar_dates,
    load_stop_times,
    load_transfers,
]


def truncate_all(): # uses the same try / commit / rollback / close pattern you know
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(TRUNCATE_SQL)
        conn.commit()
        print("Emptied all tables!")
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def main():
    start = time.time() # the current time, in seconds

    truncate_all()

    for loader in LOADERS:
        print(f"--- {loader.__name__} ---") # gives the module’s name, like scripts.load_stops, so you can see which loader is running.
        loader.load() # calls each loader's load() in LOADERS order
    
    elapsed = time.time() - start # how many seconds passed
    print(f"Refresh complete in {elapsed / 60:.1f} minutes")  # :.1f means “show 1 decimal place.” It’s handy for durations.


if __name__ == "__main__":
    main() # main() is the conventional name for a script’s “starting point” function.