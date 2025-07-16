#!/usr/bin/env python3
"""
viz.py
"""

import pandas as pd
import plotly.graph_objects as go
import os
os.chdir("Task4")
# Set working directory if needed
os.makedirs("outputs", exist_ok=True)

def load_data():
    return pd.read_csv("data/icicle_data.csv")

def preprocess_for_icicle(df):
    rows = []

    # Ensure all levels are strings and clean whitespace
    for col in ['root', 'level1', 'level2', 'level3']:
        df[col] = df[col].astype(str).str.strip()

    # Step 1: Add root
    root = df['root'].iloc[0]
    rows.append({'id': root, 'parent': '', 'value': 0})

    # Step 2: Add level1
    for level1 in df['level1'].unique():
        rows.append({'id': level1, 'parent': root, 'value': 0})

    # Step 3: Add level2
    for (level1, level2), group in df.groupby(['level1', 'level2']):
        rows.append({'id': level2, 'parent': level1, 'value': 0})

    # Step 4: Add level3 (leaf nodes with values)
    for _, row in df.iterrows():
        rows.append({
            'id': row['level3'],
            'parent': row['level2'],
            'value': row['size']
        })

    return pd.DataFrame(rows).drop_duplicates()

def create_dashboard(icicle_data):
    df = preprocess_for_icicle(icicle_data)

    fig = go.Figure(go.Icicle(
        labels=df['id'],
        parents=df['parent'],
        values=df['value'],
        tiling=dict(orientation="h"),
        textinfo="label"
    ))

    fig.update_layout(
        height=1200,
        margin=dict(t=80, l=50, r=50, b=50),
        template="plotly_white",
        font=dict(size=20, family="Arial, sans-serif", color="#333"),
        uniformtext=dict(minsize=10, mode='hide'),
        hoverlabel=dict(bgcolor="grey", font_size=16, font_family="Arial, sans-serif"),
        title_font=dict(size=24, family="Arial, sans-serif"),
        title_x=0.5,
    )

    # Step 1: Convert Plotly figure to HTML string (no full HTML)
    plot_html = fig.to_html(include_plotlyjs='cdn', full_html=False)

    # Step 2: Card CSS
    card_css = """
    <style>
    .card {
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 2px 12px rgba(50,50,93,0.07), 0 1.5px 4px rgba(0,0,0,0.07);
        padding: 18px;
        margin: 30px auto;
        max-width: 1000px;
        transition: box-shadow 0.2s;
    }
    .card:hover {
        box-shadow: 0 4px 24px rgba(50,50,93,0.13), 0 3px 8px rgba(0,0,0,0.13);
    }
    body {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f7f8fa;
    }
    </style>
    """

    # Step 3: Wrap chart in a card div
    full_html = f"""
    <html>
    <head>{card_css}</head>
    <body>
        <div class="card">
            <h2 style="margin-top: 0;">Icicle Chart: Hierarchical Data</h2>
            {plot_html}
        </div>
    </body>
    </html>
    """

    # Step 4: Write to file
    output_file = os.path.join("outputs", "icicle_chart.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Icicle chart saved to {output_file}")



if __name__ == "__main__":
    icicle_data = load_data()
    create_dashboard(icicle_data)
    print("Dashboard created successfully!")
