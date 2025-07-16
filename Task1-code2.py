import pandas as pd
import os
os.chdir("./Data/Task1")

# Load data
vehicles = pd.read_csv("vehicles.csv")
specs = pd.read_csv("specifications.csv")
performance = pd.read_csv("performance.csv")
pricing = pd.read_csv("pricing_history.csv")

# Merge 1: vehicle + specs (safe, 1:1)
merged = vehicles.merge(specs, on='vehicle_id')

# Reduce performance: keep latest or average per vehicle
performance_summary = performance.groupby('vehicle_id').agg({
    'Kilometers_Driven': 'mean',
    'mileage_num': 'mean',
    'engine_num': 'mean',
    'power_num': 'mean'
}).reset_index()

# Reduce pricing: keep latest (max year) per vehicle
latest_pricing = pricing.sort_values('Year', ascending=False).drop_duplicates('vehicle_id')

# Merge reduced performance and pricing
merged = merged.merge(performance_summary, on='vehicle_id')
merged = merged.merge(latest_pricing[['vehicle_id', 'New_Price', 'Price']], on='vehicle_id')

# Drop rows with missing prices
merged = merged.dropna(subset=['New_Price', 'Price'])

# Calculate value retention
merged['value_retention'] = merged['Price'] / merged['New_Price']

# Group and analyze
grouped = merged.groupby(['Brand', 'Fuel_Type', 'Transmission', 'Owner_Type']).agg({
    'value_retention': ['mean', 'count']
}).reset_index()

grouped.columns = ['Brand', 'Fuel_Type', 'Transmission', 'Owner_Type', 'Mean_Retention', 'Count']
print(grouped.sort_values('Mean_Retention', ascending=False).head(10))
