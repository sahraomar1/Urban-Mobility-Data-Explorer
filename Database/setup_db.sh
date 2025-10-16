#!/bin/bash
# Simple script to set up PostgreSQL database, table, and import CSV


# Fixes Windows line endings problem for this script
sed -i 's/\r$//' "$0"

# 1. Sets a password for the user who is postgres
psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'garangbse';"

# 2. Creates the database
psql -U postgres -c "CREATE DATABASE nyc_taxi;"

# 3. Grants all privileges to the postgres user
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE nyc_taxi TO postgres;"

# 4. Creates the table called trips
psql -U postgres -d nyc_taxi -c "
CREATE TABLE trips (
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

# 5. Loads the csv data into the database
psql -U postgres -d nyc_taxi -c "\copy trips(id, vendor_id, pickup_datetime, dropoff_datetime, passenger_count, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, store_and_fwd_flag, trip_duration, trip_distance_miles, average_speed_mph, pickup_hour) FROM 'cleaned_trips.csv' DELIMITER ',' CSV HEADER;"
