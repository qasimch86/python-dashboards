#!/usr/bin/env python3
"""
data_gen.py
"""

import numpy as np
import pandas as pd
import os
os.chdir("Task4")

def generate_icicle_data(filename="data/icicle_data.csv"):
    root = "flare"
    level1 = ["vis", "util", "animate",  "query", "analytics", "scale", "physics", "display"]
    level2 = {
        "vis": ["d3", "three.js", "plotly"],
        "util": ["lodash", "moment", "axios"],
        "animate": ["anime.js", "gsap"],
        "query": ["sql.js", "mongo"],
        "analytics": ["google-analytics", "mixpanel"],
        "scale": ["d3-scale", "chart.js"],
        "physics": ["matter.js", "cannon.js"],
        "display": ["react", "vue", "angular"]
    }

    rows = []
    for l1 in level1:
        if l1 in level2:
            for l2 in level2[l1]:
                level2_size = np.random.randint(50, 300)
                rows.append([root, l1, l2, level2_size])

    df = pd.DataFrame(rows, columns=["root", "level1", "level2", "size"])
    df.to_csv(filename, index=False)


def main():
    generate_icicle_data()
    print("Icicle data generated successfully.")

if __name__ == "__main__":
    main()
