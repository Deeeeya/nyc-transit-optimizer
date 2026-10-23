import os # import [] brings in the whole package
import psycopg2
import dotenv

dotenv.load_dotenv() # python-dotenv has a function called load_dotenv() that reads your .env file

def get_connection():
    url = os.environ["DATABASE_URL"] # how you grab an environment variable in Python, if the variable is optional, then best practice is to use .get(""), however if its mandatory like the URL, use [] without .get
    conn = psycopg2.connect(url) # opens the database connection
    return conn