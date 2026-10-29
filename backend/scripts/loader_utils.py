from psycopg2.extras import execute_values
from database import get_connection

def bulk_insert(sql, rows, label, page_size=1000):
    conn = get_connection() # This calls your function from database.py, and the connection it returns gets stored in conn.
    cur = conn.cursor() # curr (the cursor) is what actually speaks SQL over that line. You send queries through it.

    try: # attempt the work
        execute_values(cur, sql, rows, page_size=page_size) # With this, your SQL has one single %s after VALUES, and it fills in all the rows for you.
        conn.commit()
        print(f"Loaded {len(rows)} {label} (existing ones skipped)") # The f before the quotes lets you put variables inside { }. It’s the same as JS template literals: `Loaded ${count} stops`.
    except Exception: # something broke → undo it
        conn.rollback() # if something breaks halfway, it cancels everything, so you never end up with half a table
        print("Something went wrong, rolled back. Nothing was saved.")
        raise # re-shows the original error after rolling back, so you can still see what went wrong.
    finally: # ALWAYS runs, success or failure → clean up
        cur.close()
        conn.close()