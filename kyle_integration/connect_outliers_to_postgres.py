import psycopg2
import pandas as pd

# Step 1: Load your outlier trips data
outliers_df = pd.read_csv("outlier_trips.csv")

# Step 2: Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="nyc_taxi",
        user="postgres",
        password="garangbuke",  
        host="localhost",
        port="5432"
    )
    print(" Connected to PostgreSQL database successfully!")
except Exception as e:
    print("❌ Error connecting to database:", e)
    exit()

# Step 3: Create a cursor to interact with the database
cur = conn.cursor()

# Step 4: Create a table for outlier trips (if it doesn't exist yet)
create_table_query = """
CREATE TABLE IF NOT EXISTS outlier_trips (
    trip_id VARCHAR(50),
    trip_distance_miles FLOAT,
    average_speed_mph FLOAT
);
"""
cur.execute(create_table_query)
conn.commit()
print(" Table 'outlier_trips' ready!")

# Step 5: Insert the outlier data into the database
for _, row in outliers_df.iterrows():
    cur.execute(
        "INSERT INTO outlier_trips (trip_id, trip_distance_miles, average_speed_mph) VALUES (%s, %s, %s)",
        (row['trip_id'], row['trip_distance_miles'], row['average_speed_mph'])
    )

conn.commit()
print(f" Inserted {len(outliers_df)} outlier records into database!")

# Step 6: Close connection
cur.close()
conn.close()
print(" Connection closed.")
