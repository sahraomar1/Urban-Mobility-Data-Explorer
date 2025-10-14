#!/bin/bash
#The script creates all the database tables and copies the data into it as well
# 1. Create the database
psql -U postgres -c "CREATE DATABASE nyc_taxi;"

# 2. Create the table
psql -U postgres -d nyc_taxi -c "
CREATE TABLE IF NOT EXISTS trips (
    id VARCHAR(20) PRIMARY KEY,
    vendor_id SMALLINT,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count SMALLINT,
    pickup_longitude DECIMAL(9,6),
    pickup_latitude DECIMAL(9,6),
    dropoff_longitude DECIMAL(9,6),
    dropoff_latitude DECIMAL(9,6),
    store_and_fwd_flag BOOLEAN,
    trip_duration INT,
    trip_distance_miles DECIMAL(6,2),
    average_speed_mph DECIMAL(5,2),
    pickup_hour SMALLINT
);
"

# 3. Load the CSV data
psql -U postgres -d nyc_taxi -c "\copy trips(id, vendor_id, pickup_datetime, dropoff_datetime, passenger_count, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, store_and_fwd_flag, trip_duration, trip_distance_miles, average_speed_mph, pickup_hour) FROM 'cleaned_trips.csv' DELIMITER ',' CSV HEADER;"