from fastapi import FastAPI
from pydantic import BaseModel
import os, psycopg2

app = FastAPI()

# Hämta databas-url
DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/")
def read_root():
    return {"message": "Hello, Emma! Your backend is running."}

# En enkel test-endpoint för att visa att DB funkar
@app.get("/dbtest")
def db_test():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        conn.close()
        return {"database_time": str(result[0])}
    except Exception as e:
        return {"error": str(e)}
    