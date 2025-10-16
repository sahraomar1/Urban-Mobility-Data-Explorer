# NYC Taxi Trip 
# Overview

This first part handles cleaning the 2016 NYC Yellow Cab dataset (train.csv) for our Urban Mobility Data Explorer website. data_cleaner.py, processes the raw data, removes bad records, adds three new features (trip_distance_miles, average_speed_mph, pickup_hour), and saves the cleaned data for the website’s database and visualizations.

# Setup Instructions for Running the Data Cleaning

These steps show you how to set up and run our data cleaning script to get the cleaned data for the website.

1. Get Python Ready:

- Make sure you have Python 3.8 or higher installed 
python --version



2. Install Required Libraries:

- pip install pandas numpy


3. Set Up the Folder:


- Clone our project repo: https://github.com/sahraomar1/Urban-Mobility-Data-Explorer.git.

- Go to the data_processing/ folder in the repo.

- Download train.csv from Kaggle: https://www.kaggle.com/c/nyc-taxi-trip-duration/data

- Place train.csv in the data_processing/ folder alongside data_cleaner.py.


4. Run the Cleaning Script:

- cd data_processing

- python data_cleaner.py

- The script will clean train.csv (1,458,644 trips) and create two files in data_processing/:

- cleaned_trips.csv: Cleaned data (1,437,260 trips, 14 columns) for the website’s database.

- excluded_logs.csv: Log of 21,384 removed trips with reasons (for transparency).



### SETUP INSTRUCTIONS 
# CLONE REPOSITORY 
- git clone https://github.com/sahraomar1/Urban-Mobility-Data-Explorer.git
- cd Urban-Mobility-Data-Explorer


# TO INSTALL THE CLEANED_CSV FILE TO THE DATABASE FOLDER
- install_cleaned_trips_csv.sh

# to install  postgress (wsl)
- sudo apt update
- sudo apt install postgresql postgresql-contrib 

# Start PostgreSQL
- sudo service postgresql start

# to Run the database creation script
- cd Database
- chmod +x setup_db.sh
- bash setup_db.sh

# create python environment
- cd Urban-Mobility-Data-Explorer
- run python3 -m venv venv

# activate python environment
## Linux / WSL / macOS
- source venv/bin/activate

## Windows (CMD) 
- venv\Scripts\activate.bat

## Windows (PowerShell)
- venv\Scripts\Activate.ps1

# to install required packages
- pip install -r requirements.txt

# to run the api
- cd API
- uvicorn trips_api:app --reload --port 8003


# Outputs for the Website

- cleaned_trips.csv: Contains 1,437,260 trips with 14 columns:

- Original: id, vendor_id, pickup_datetime, dropoff_datetime, passenger_count, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, store_and_fwd_flag, trip_duration.

- New Features: trip_distance_miles (trip length in miles), average_speed_mph (speed in mph), pickup_hour (hour of pickup).

- excluded_logs.csv: Shows why 21,384 trips were removed (e.g., invalid coordinates, unrealistic speeds).


- Access: These files are too big for GitHub (>100 MB), so they can't be pushed to GitHub. Get them from https://drive.google.com/drive/folders/1P_xxrjYAfn7RiogkCTrDSo_FxsumYnLr
