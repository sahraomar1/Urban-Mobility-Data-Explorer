from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import psycopg2.extras

# -----------------------------
# Step 1: Create the FastAPI app
# -----------------------------
app = FastAPI()

# Allow access from anywhere (helps when using HTML frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Step 2: Database connection helper
# -----------------------------
def get_db_cursor():
    """
    Opens a connection to your PostgreSQL database and returns a cursor.
    The cursor is what lets you run SQL commands like SELECT or INSERT.
    """
    db = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="garangbuke",  # double-check spelling
        dbname="nyc_taxi"
    )
    return db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# -----------------------------
# ✅ Step 3: Add endpoint to view outlier trips
# -----------------------------
@app.get("/outliers")
def get_outliers(limit: int = 100):
    """
    This function runs when you visit:
    http://127.0.0.1:8000/outliers
    It grabs rows from the 'outlier_trips' table in your PostgreSQL database.
    """
    cursor = get_db_cursor()
    cursor.execute("SELECT * FROM outlier_trips LIMIT %s", (limit,))
    outliers = cursor.fetchall()
    cursor.connection.close()

    if not outliers:
        raise HTTPException(status_code=404, detail="No outlier trips found")

    return outliers
