\c nyc_taxi

\copy trips(id, vendor_id, pickup_datetime, dropoff_datetime, passenger_count, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, store_and_fwd_flag, trip_duration, trip_distance_miles, average_speed_mph, pickup_hour) FROM 'cleaned_trips.csv' DELIMITER ',' CSV HEADER;   