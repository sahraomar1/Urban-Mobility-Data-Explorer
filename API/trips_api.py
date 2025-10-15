# importing fast api and psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
import psycopg2
import psycopg2.extras



app = FastAPI()


# It tells the API to accept
# requests from any origin, which is needed when you open the HTML file directly. 
# An issue that is often found in chromium based browsers related to security.
origins = ["*"] # Allows all origins, including 'null'

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)



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

# Code added by Rajveer for API: Allows for daily aggregation of trip counts

# A helper function to avoid repeating the database connection logic
def get_db_cursor():
    db = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="garangbse",
        dbname="nyc_taxi"
    )
    return db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


@app.get("/dates")
def get_date_range():
    """
    so dhsbasicall this help us finds the first and last trip dates in the entire dataset.
    This is used to set the boundaries of the date picker. Its important so that user doesn't look for dates and there is no data for those dates.
    """
    cursor = get_db_cursor()
    query = "SELECT MIN(pickup_datetime)::date as min_date, MAX(pickup_datetime)::date as max_date FROM trips"
    cursor.execute(query)
    dates = cursor.fetchone()
    cursor.connection.close()
    return dates

@app.get("/stats")
def get_stats(date: str):
    """
    Calculates all key statistics for a single date, converting units (initially these were in miles) to kilometers.
    """
    cursor = get_db_cursor()
    MILES_TO_KM = 1.60934 # Conversion factor
    
    # now calculates all stats and converts miles to km
    stats_query = f"""
        SELECT
            COUNT(*) AS total_trips,
            SUM(passenger_count) AS total_passengers,
            AVG(passenger_count) AS avg_passengers_per_trip,
            SUM(trip_distance_miles * {MILES_TO_KM}) AS total_distance_km,
            AVG(trip_duration) / 60 AS avg_trip_duration_mins,
            AVG((trip_distance_miles * {MILES_TO_KM}) / NULLIF(trip_duration / 3600.0, 0)) AS avg_speed_kph
        FROM trips
        WHERE pickup_datetime::date = %s;
    """
    cursor.execute(stats_query, (date,))
    stats = cursor.fetchone()

    # A separate, quick query to find the busiest hour
    busiest_hour_query = """
        SELECT EXTRACT(HOUR FROM pickup_datetime) as hour
        FROM trips
        WHERE pickup_datetime::date = %s
        GROUP BY hour ORDER BY COUNT(*) DESC LIMIT 1;
    """
    cursor.execute(busiest_hour_query, (date,))
    busiest_hour_result = cursor.fetchone()
    stats['busiest_hour'] = int(busiest_hour_result['hour']) if busiest_hour_result else None
    
    cursor.connection.close()

    # Calculate final stat safely
    if stats and stats['total_passengers'] and stats['total_passengers'] > 0 and stats['total_distance_km'] is not None:
        stats['avg_dist_per_passenger_km'] = stats['total_distance_km'] / stats['total_passengers']
    else:
        stats['avg_dist_per_passenger_km'] = 0
    
    return stats

@app.get("/trips_by_hour")
def get_trips_by_hour(date: str):
    """
    Counts how many trips occurred in each of the 24 hours of a given day.
    This powers the bar chart.
    """
    cursor = get_db_cursor()
    query = """
        SELECT EXTRACT(HOUR FROM pickup_datetime) as hour, COUNT(*) as count
        FROM trips
        WHERE pickup_datetime::date = %s
        GROUP BY hour
        ORDER BY hour;
    """
    cursor.execute(query, (date,))
    results = cursor.fetchall()
    cursor.connection.close()
    
    # Ensure all 24 hours are present, even if they have 0 trips
    hourly_counts = {hour: 0 for hour in range(24)}
    for row in results:
        hourly_counts[int(row['hour'])] = row['count']
        
    return [{"hour": hour, "count": count} for hour, count in hourly_counts.items()]

@app.get("/map_data")
def get_map_data(date: str):
    """
    Gets the pickup coordinates for trips on a given day.
    A LIMIT is used because a single day can have too many trips to plot.
    """
    cursor = get_db_cursor()
    query = "SELECT pickup_latitude, pickup_longitude FROM trips WHERE pickup_datetime::date = %s LIMIT 1000;"
    cursor.execute(query, (date,))
    map_data = cursor.fetchall()
    cursor.connection.close()
    return map_data

@app.get("/trip/{trip_id}")
def get_single_trip(trip_id: str):
    """
    Finds a single trip and converts its distance to kilometers.
    """
    cursor = get_db_cursor()
    MILES_TO_KM = 1.60934
    
    query = f"""
        SELECT id, pickup_datetime, dropoff_datetime, passenger_count,
               (trip_distance_miles * {MILES_TO_KM}) as trip_distance_km,
               trip_duration, pickup_latitude, pickup_longitude,
               dropoff_latitude, dropoff_longitude
        FROM trips WHERE id = %s;
    """
    cursor.execute(query, (trip_id,))
    trip = cursor.fetchone()
    cursor.connection.close()
    
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip