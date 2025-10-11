# data_cleaner.py
# Cleans the NYC Yellow Cab dataset (train.csv)
# Outputs: cleaned_trips.csv (cleaned data), excluded_logs.csv (excluded records).

import pandas as pd
import numpy as np
from datetime import datetime
import math  # For Haversine distance calculation

# Helper function: Calculate Haversine distance (miles) between two lat-long points
def haversine_distance(lat1, lon1, lat2, lon2):
    # Earth's radius in miles
    R = 3958.8
    # Convert degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    # Differences
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    # Haversine formula
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    distance = R * c
    return distance

# Step 1: Load the raw data
print("Loading train.csv...")
try:
    df = pd.read_csv('train.csv')
except FileNotFoundError:
    print("Error: train.csv not found. Please place it in the same folder.")
    exit()

# Show basic info
print("Original data shape:", df.shape)
print("First few rows:\n", df.head())

# Step 2: Parse datetime columns
print("Parsing datetimes...")
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors='coerce')
df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'], errors='coerce')

# Step 3: Initialize list for excluded records
excluded = []

# Step 4: Handle missing values
critical_columns = ['id', 'vendor_id', 'pickup_datetime', 'dropoff_datetime', 'passenger_count',
                    'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude']
missing_mask = df[critical_columns].isnull().any(axis=1)
for idx in df[missing_mask].index:
    excluded.append({'row_index': idx, 'reason': 'Missing critical value', 'data': df.loc[idx].to_dict()})
df = df[~missing_mask]
print(f"Removed {sum(missing_mask)} rows with missing values.")

# Step 5: Remove duplicates
dupe_mask = df['id'].duplicated()
for idx in df[dupe_mask].index:
    excluded.append({'row_index': idx, 'reason': 'Duplicate ID', 'data': df.loc[idx].to_dict()})
df = df[~dupe_mask]
print(f"Removed {sum(dupe_mask)} duplicate rows.")

# Step 6: Filter invalid records
invalid_mask = (
    (df['passenger_count'] < 1) | (df['passenger_count'] > 6) |
    (df['trip_duration'] <= 30) | (df['trip_duration'] > 86400) |
    (df['vendor_id'].isin([1, 2]) == False) |
    (df['store_and_fwd_flag'].isin(['Y', 'N']) == False)
)
for idx in df[invalid_mask].index:
    excluded.append({'row_index': idx, 'reason': 'Invalid value (e.g., passenger count, duration)', 'data': df.loc[idx].to_dict()})
df = df[~invalid_mask]
print(f"Removed {sum(invalid_mask)} rows with invalid values.")

# Step 7: Filter invalid coordinates
coord_mask = (
    (df['pickup_latitude'] < 40.4) | (df['pickup_latitude'] > 40.9) |
    (df['pickup_longitude'] > -73.7) | (df['pickup_longitude'] < -74.3) |
    (df['dropoff_latitude'] < 40.4) | (df['dropoff_latitude'] > 40.9) |
    (df['dropoff_longitude'] > -73.7) | (df['dropoff_longitude'] < -74.3)
)
for idx in df[coord_mask].index:
    excluded.append({'row_index': idx, 'reason': 'Coordinates outside NYC', 'data': df.loc[idx].to_dict()})
df = df[~coord_mask]
print(f"Removed {sum(coord_mask)} rows with invalid coordinates.")

# Step 8: Calculate derived feature: Trip distance (miles)
print("Calculating trip distances...")
df['trip_distance_miles'] = df.apply(
    lambda row: haversine_distance(
        row['pickup_latitude'], row['pickup_longitude'],
        row['dropoff_latitude'], row['dropoff_longitude']
    ), axis=1
)
dist_mask = (df['trip_distance_miles'] < 0.1) | (df['trip_distance_miles'] > 50)
for idx in df[dist_mask].index:
    excluded.append({'row_index': idx, 'reason': 'Unrealistic trip distance', 'data': df.loc[idx].to_dict()})
df = df[~dist_mask]
print(f"Removed {sum(dist_mask)} rows with unrealistic distances.")

# Step 9: Filter outliers based on speed
df['average_speed_mph'] = df['trip_distance_miles'] / (df['trip_duration'] / 3600)
speed_mask = (df['average_speed_mph'] > 100) | (df['average_speed_mph'] < 1)
for idx in df[speed_mask].index:
    excluded.append({'row_index': idx, 'reason': 'Unrealistic speed', 'data': df.loc[idx].to_dict()})
df = df[~speed_mask]
print(f"Removed {sum(speed_mask)} rows with unrealistic speeds.")

# Step 10: Add derived feature: Time of day (hour)
df['pickup_hour'] = df['pickup_datetime'].dt.hour

# Step 11: Normalize formats
df['passenger_count'] = df['passenger_count'].astype(int)
df['vendor_id'] = df['vendor_id'].astype(int)
df['trip_distance_miles'] = df['trip_distance_miles'].round(2)
df['average_speed_mph'] = df['average_speed_mph'].round(2)
df['trip_duration'] = df['trip_duration'].astype(int)

# Step 12: Log excluded records
if excluded:
    excluded_df = pd.DataFrame(excluded)
    excluded_df.to_csv('excluded_logs.csv', index=False)
    print(f"Logged {len(excluded)} excluded records to excluded_logs.csv")
else:
    print("No excluded records.")

# Step 13: Save cleaned data
df = df.reset_index(drop=True)
df.to_csv('cleaned_trips.csv', index=False)
print("Cleaned data saved to cleaned_trips.csv")
print("Final data shape:", df.shape)
print("Columns in cleaned data:", list(df.columns))