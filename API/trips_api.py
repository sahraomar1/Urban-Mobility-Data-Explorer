# importing fast api and psycopg2
from fastapi import FastAPI, HTTPException
import psycopg2
import psycopg2.extras

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# For connecting to PostgreSQL
db = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="postgres",  # for setting your password
    dbname="nyc_taxi"
)
cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# available endpoints
@app.get("/trips")
def get_trips(limit: int = 100):
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

@app.get("/dates")
def get_available_dates():
    """
    Returns the min/max dates, and also the most recent date
    that is guaranteed to have trips.
    """
    query = """
        WITH DateRange AS (
            SELECT
                MIN(pickup_datetime)::date as min_date,
                MAX(pickup_datetime)::date as max_date
            FROM trips
        ),
        LastValidDate AS (
            SELECT pickup_datetime::date as last_valid_date
            FROM trips
            GROUP BY 1
            ORDER BY 1 DESC
            LIMIT 1
        )
        SELECT * FROM DateRange, LastValidDate;
    """
    cursor.execute(query)
    dates = cursor.fetchone()
    if not dates:
        raise HTTPException(status_code=404, detail="No dates found.")
    return dates

@app.get("/stats")
def get_stats(date: str):
    query = """
        SELECT
            COALESCE(COUNT(id), 0) AS total_trips,
            COALESCE(SUM(passenger_count), 0) AS total_passengers,
            COALESCE(AVG(passenger_count), 0) AS avg_passengers_per_trip,
            COALESCE(SUM(trip_distance_miles), 0) AS total_distance_miles,
            COALESCE(SUM(trip_distance_miles) / NULLIF(SUM(passenger_count), 0), 0) AS avg_dist_per_passenger
        FROM trips
        WHERE pickup_datetime::date = %s;
    """
    cursor.execute(query, (date,))
    stats = cursor.fetchone()
    if not stats:
        raise HTTPException(status_code=404, detail=f"No data for date {date}.")
    return stats

@app.get("/trips_by_hour")
def get_trips_by_hour(date: str):
  
    query = """
        SELECT
            EXTRACT(hour FROM pickup_datetime) AS hour,
            COUNT(*) AS trip_count
        FROM trips
        WHERE pickup_datetime::date = %s
        GROUP BY hour
        ORDER BY hour;
    """
    cursor.execute(query, (date,))
    hourly_data = cursor.fetchall()

    # Fills in hours with 0 trips if no trips occurred
    result = {hour: 0 for hour in range(24)}
    for row in hourly_data:
        result[row['hour']] = row['trip_count']

    return [{"hour": h, "count": c} for h, c in result.items()]

@app.get("/map_data")
def get_map_data(date: str):
   
    query = """
        SELECT id, pickup_latitude, pickup_longitude
        FROM trips
        WHERE pickup_datetime::date = %s
        LIMIT 500;
    """
    cursor.execute(query, (date,))
    return cursor.fetchall()

@app.get("/trip/{trip_id}")
def get_trip_by_id(trip_id: str):

    query = "SELECT * FROM trips WHERE id = %s;"
    cursor.execute(query, (trip_id,))
    trip = cursor.fetchone()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found.")
    return trip