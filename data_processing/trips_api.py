# importing fast api and psycopg2
from fastapi import FastAPI
import psycopg2
import psycopg2.extras

app = FastAPI()

# For connecting to PostgreSQL
db = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="garangbse",  # for setting your password
    dbname="nyc_taxi"
)
cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# available endpoints
@app.get("/trips")
def get_id(limit: int = 100):
    cursor.execute(f"SELECT * FROM trips LIMIT {limit}")
    return cursor.fetchall()

@app.get("/trips/id")
def get_id(limit: int = 100):
    cursor.execute(f"SELECT id FROM trips LIMIT {limit}")
    return cursor.fetchall()

@app.get("/trips/pickup_datetime")
def get_pickup_datetime(limit: int = 100):
    cursor.execute(f"SELECT id, pickup_datetime FROM trips LIMIT {limit}")
    return cursor.fetchall()

@app.get("/trips/dropoff_datetime")
def get_dropoff_datetime(limit: int = 100):
    cursor.execute(f"SELECT id, dropoff_datetime FROM trips LIMIT {limit}")
    return cursor.fetchall()

@app.get("/trips/passenger_count")
def get_passenger_count(limit: int = 100):
    cursor.execute(f"SELECT id, passenger_count FROM trips LIMIT {limit}")
    return cursor.fetchall()

@app.get("/trips/pickup_longitude")
def get_pickup_longitude(limit: int = 100):
    cursor.execute(f"SELECT id, pickup_longitude FROM trips LIMIT {limit}")
    return cursor.fetchall()

@app.get("/trips/pickup_latitude")
def get_pickup_latitude(limit: int = 100):
    cursor.execute(f"SELECT id, pickup_latitude FROM trips LIMIT {limit}")
    return cursor.fetchall()

@app.get("/trips/dropoff_longitude")
def get_dropoff_longitude(limit: int = 100):
    cursor.execute(f"SELECT id, dropoff_longitude FROM trips LIMIT {limit}")
    return cursor.fetchall()

@app.get("/trips/dropoff_latitude")
def get_dropoff_latitude(limit: int = 100):
    cursor.execute(f"SELECT id, dropoff_latitude FROM trips LIMIT {limit}")
    return cursor.fetchall()

@app.get("/trips/trip_duration")
def get_trip_duration(limit: int = 100):
    cursor.execute(f"SELECT id, trip_duration FROM trips LIMIT {limit}")
    return cursor.fetchall()

@app.get("/trips/trip_distance_miles")
def get_trip_distance_miles(limit: int = 100):
    cursor.execute(f"SELECT id, trip_distance_miles FROM trips LIMIT {limit}")
    return cursor.fetchall()
