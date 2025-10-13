-- Create and connect to the database (psql)
CREATE DATABASE nyc_taxi;
\c nyc_taxi;

-- Create the trips table
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

-- Indexes
CREATE INDEX idx_trips_pickup_datetime ON trips(pickup_datetime);
CREATE INDEX idx_trips_dropoff_datetime ON trips(dropoff_datetime);
CREATE INDEX idx_trips_vendor ON trips(vendor_id);
CREATE INDEX idx_trips_passenger_count ON trips(passenger_count);
CREATE INDEX idx_trips_trip_duration ON trips(trip_duration);
CREATE INDEX idx_trips_coords ON trips(pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude);
