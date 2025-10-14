# to run the api 
## on python terminal
cd to API directory 
run C:/Python313/python.exe -m uvicorn API.trips_api:app --reload   

# to start db 
## on wsl
put the cleaned_trips.csv file in the Database directory
run the script setupdb.sh

### required python packages
fastapi==0.119.0
uvicorn==0.37.0
psycopg2-binary==2.9.9
