# outlier_detection.py

import pandas as pd

# Step 1: Load the cleaned trips data
file_path = "data_processing/cleaned_trips.csv"
df = pd.read_csv(file_path)

# Step 2: Display the first few rows
print("Here are the first few rows of the data:")
print(df.head())

# Step 3: Find trips with average speed < 2 or > 70
outliers = df[(df["average_speed_mph"] > 70) | (df["average_speed_mph"] < 2)]

# Step 4: Show how many outliers were found
print(f"Number of outlier trips found: {len(outliers)}")

# Step 5: Save them into a new CSV file
outliers.to_csv("outlier_trips.csv", index=False)

print("Saved results to: outlier_trips.csv")
