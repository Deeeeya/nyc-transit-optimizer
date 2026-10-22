from fastapi import FastAPI # using 'from' brings in one specific function from a package
import os # import [] brings in the whole package
import psycopg2
import dotenv 

dotenv.load_dotenv() # python-dotenv has a function called load_dotenv() that reads your .env file
url = os.environ.get("DATABASE_URL") # how you grab an environment variable in Python
conn = psycopg2.connect(url) # opens the database connection

app = FastAPI()

@app.get("/") # The @app.get("/") line is called a decorator. It attaches extra behavior to the function right below it. Here it tells FastAPI: “When someone sends a GET request to /, run this function.”
def read_root():
    return {"message": "Transit API is running!"} # FastAPI automatically turns dictionaries into JSON, which is why you saw it in the browser.

# What this does: You’re creating a FastAPI app and defining one route — 
# a GET request to / that just returns a simple message. It’s the Python 
# equivalent of what you did in Taskflow when you set up your first Express route. 
# Just a “hello world” to prove the server works.