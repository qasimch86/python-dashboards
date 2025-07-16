#!/usr/bin/env python3
"""
data_gen.py
"""

import numpy as np
import pandas as pd
import os
os.chdir("Task4")
os.makedirs("data", exist_ok=True)

def generate_hierarchical_data(filename="data/icicle_data.csv"):
    root = "flare"
    level1 = ["vis", "util", "animate", "query", "analytics", "scale", "physics", "display"]
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

    level3_options = {
        "d3": ["shapes", "controls", "axis"],
        "three.js": ["render", "scene", "camera"],
        "plotly": ["scatter", "bar", "surface"],
        "lodash": ["map", "filter", "reduce"],
        "moment": ["format", "parse", "diff"],
        "axios": ["get", "post", "interceptors"],
        "anime.js": ["timeline", "easing", "events"],
        "gsap": ["tween", "timeline", "scrollTrigger"],
        "sql.js": ["select", "insert", "delete"],
        "mongo": ["find", "aggregate", "update"],
        "google-analytics": ["event", "pageview", "goal"],
        "mixpanel": ["track", "alias", "identify"],
        "d3-scale": ["linear", "log", "ordinal"],
        "chart.js": ["datasets", "legends", "scales"],
        "matter.js": ["bodies", "engine", "collision"],
        "cannon.js": ["world", "body", "constraint"],
        "react": ["hooks", "context", "components"],
        "vue": ["directives", "vuex", "components"],
        "angular": ["modules", "services", "directives"]
    }

    rows = []
    for l1 in level1:
        for l2 in level2.get(l1, []):
            for l3 in level3_options.get(l2, []):
                size = np.random.randint(20, 200)
                rows.append([root, l1, l2, l3, size])

    df = pd.DataFrame(rows, columns=["root", "level1", "level2", "level3", "size"])
    df.to_csv(filename, index=False)
    print(f"Data written to: {filename}")

def main():
    generate_hierarchical_data()

if __name__ == "__main__":
    main()
