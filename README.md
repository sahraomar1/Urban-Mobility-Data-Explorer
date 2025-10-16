# NYC Taxi Trip Data Processing
# Overview

This part handles cleaning the 2016 NYC Yellow Cab dataset (train.csv) for our Urban Mobility Data Explorer website. My script, data_cleaner.py, processes the raw data, removes bad records, adds three new features (trip_distance_miles, average_speed_mph, pickup_hour), and saves the cleaned data for the website’s database and visualizations.

# Setup Instructions for Running the Data Cleaning

These steps show you how to set up and run my data cleaning script to get the cleaned data for the website.

1. Get Python Ready:

Make sure you have Python 3.8 or higher installed 
python --version



2. Install Required Libraries:

pip install pandas numpy


3. Set Up the Folder:


Clone our project repo: https://github.com/sahraomar1/Urban-Mobility-Data-Explorer.git.

Go to the data_processing/ folder in the repo.

Download train.csv from Kaggle: https://www.kaggle.com/c/nyc-taxi-trip-duration/data

Place train.csv in the data_processing/ folder alongside data_cleaner.py.


4. Run the Cleaning Script:

Open VS Code and navigate to data_processing/data_cleaner.py.

Run the script by right-clicking data_cleaner.py and selecting “Run Python File in Terminal” or type in the terminal:

cd data_processing
python data_cleaner.py


The script will clean train.csv (1,458,644 trips) and create two files in data_processing/:

cleaned_trips.csv: Cleaned data (1,437,260 trips, 14 columns) for the website’s database.

excluded_logs.csv: Log of 21,384 removed trips with reasons (for transparency).

# Outputs for the Website

cleaned_trips.csv: Contains 1,437,260 trips with 14 columns:

Original: id, vendor_id, pickup_datetime, dropoff_datetime, passenger_count, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, store_and_fwd_flag, trip_duration.

New Features: trip_distance_miles (trip length in miles), average_speed_mph (speed in mph), pickup_hour (hour of pickup).

excluded_logs.csv: Shows why 21,384 trips were removed (e.g., invalid coordinates, unrealistic speeds).


Access: These files are too big for GitHub (>100 MB), so we couldn't push to GitHub. Get them from https://drive.google.com/drive/folders/1P_xxrjYAfn7RiogkCTrDSo_FxsumYnLr

# to run the api 
## on python terminal
cd to API directory 
run C:/Python313/python.exe -m uvicorn API.trips_api:app --reload --port 8003

# to start db 
## on wsl
put the cleaned_trips.csv file in the Database directory
run the script setupdb.sh

### required python packages
fastapi==0.119.0
uvicorn==0.37.0
psycopg2-binary==2.9.9
