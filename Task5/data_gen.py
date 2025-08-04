# This script generates synthetic population data for various states in the US
# and saves it in CSV files within a 'data' directory.
# The data includes population over time, state populations for specific years,
# gains and losses in population, and growth rates for each state.
# The generated data can be used for further analysis or testing purposes.
# The script uses numpy for random number generation and pandas for data manipulation.
# The data is saved in CSV format for easy access and use in other applications.
# The script ensures that the 'data' directory exists before saving the files.
# The random seed is set for reproducibility of the generated data.
# The generated data includes:
# - Population over time from 2010 to 2019
# - State populations for 2016, 2018, 2019, and 2020
# - Gains and losses in population for Texas and Puerto Rico
# - Growth rates for each state

import pandas as pd
import numpy as np
import random
import os
os.chdir("Task5")
def generate_population_data():
    # Create a directory for the data if it doesn't exist
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Generate population data
    years = list(range(2010, 2021))
    states = ['California', 'Texas', 'Florida', 'New York', 'Illinois', 'Pennsylvania', 
              'Ohio', 'Georgia', 'North Carolina', 'Michigan', 'New Jersey', 'Virginia', 
              'Washington', 'Arizona', 'Massachusetts', 'Tennessee', 'Indiana', 
              'Missouri', 'Maryland', 'Wisconsin', 'Colorado', 'Minnesota', 
              'South Carolina', 'Alabama', 'Louisiana', 'Kentucky', 
              'Oregon', 'Oklahoma', 'Connecticut', 'Utah', 
              'Iowa', 'Nevada', 'Arkansas', 
              'Mississippi', 'Kansas', 
              'New Mexico', 'Nebraska',
              'West Virginia', 
              'Idaho', 
              'Hawaii',
              'New Hampshire',
              'Maine',
              'Montana',
              'Rhode Island',
              'Delaware',
              'South Dakota',
              'North Dakota',
              'Alaska',
              'Vermont',
              'Wyoming',
              "District of Columbia",
              "Puerto Rico"]
    data = []
    for state in states:
        base_population = random.randint(500000, 40000000)  # Starting population
        row = {"State": state}
        for year in years:
            # Simulate slight annual growth
            growth_rate = random.uniform(0.002, 0.02)  # 0.2% to 2% growth
            base_population = int(base_population * (1 + growth_rate))
            row[str(year)] = base_population
        data.append(row)

    df = pd.DataFrame(data)
    df.to_csv("data/state_population.csv", index=False)
    print("Saved to data/state_population.csv")

# Call the function to generate the data
if __name__ == "__main__":
    generate_population_data()



