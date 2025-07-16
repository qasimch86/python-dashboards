import pandas as pd
import numpy as np
import os
os.chdir("Task2")

def generate_sunburst_data(filename="sunburst_data.csv", seed=42):
    np.random.seed(seed)

    regions = ["Central", "East", "West", "South"]
    categories = ["Furniture", "Office Supplies", "Technology"]
    sub_categories = {
        "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
        "Office Supplies": ["Binders", "Paper", "Envelopes", "Labels", "Storage"],
        "Technology": ["Phones", "Accessories", "Machines", "Copiers"]
    }

    rows = []
    for region in regions:
        for category in categories:
            for sub_cat in sub_categories[category]:
                sales = np.round(np.random.uniform(10000, 50000), 2)
                rows.append([region, category, sub_cat, sales])

    df = pd.DataFrame(rows, columns=["Region", "Category", "Sub-Category", "Sales"])
    df.to_csv(filename, index=False)
    print(f"Saved sunburst data to {filename}")

if __name__ == "__main__":
    generate_sunburst_data()
