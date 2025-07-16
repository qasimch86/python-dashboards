#!/usr/bin/env python3
"""
viz.py
"""

import pandas as pd
import plotly.graph_objects as go
import os
os.chdir("Task4")
def load_data():
    df1 = pd.read_csv("data/icicle_data.csv")
    return df1

def preprocess_for_icicle(df):
    rows = []

    # Force all to string and strip spaces to avoid mismatch
    df['root'] = df['root'].astype(str).str.strip()
    df['level1'] = df['level1'].astype(str).str.strip()
    df['level2'] = df['level2'].astype(str).str.strip()

    # Step 1: Add root
    rows.append({'id': 'flare', 'parent': '', 'value': 0})

    # Step 2: Add level1
    for level1 in df['level1'].dropna().unique():
        rows.append({'id': level1, 'parent': 'flare', 'value': 0})

    # Step 3: Add level2
    for _, row in df.iterrows():
        if pd.notna(row['level2']):
            rows.append({
                'id': row['level2'],
                'parent': row['level1'],
                'value': row['size']
            })

    return pd.DataFrame(rows).drop_duplicates()


def create_dashboard(icicle_data):
    # Icicle Chart ─────────────────────────────────────
    df = preprocess_for_icicle(icicle_data)
    # Create the icicle chart using Plotly
    # The 'labels' will be the leaf nodes, 'parents' will be the parent nodes,
    # and 'values' will be the size of each node.
    print(df[['id', 'parent', 'value']])

    fig = go.Figure(go.Icicle(
    labels=df['id'],
    parents=df['parent'],
    values=df['value'],
    # branchvalues="total",
    tiling=dict(orientation="v"),  # horizontal layers as you requested
    textinfo="label+value+percent entry"
))

    fig.update_layout(
        title="Icicle Chart of Data Hierarchy",
        height=600,
        margin=dict(t=20, l=20, r=20, b=20),
        template="plotly_white",
        uniformtext=dict(minsize=10, mode='show'),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )
    

    fig.update_layout(
    title=dict(
        font=dict(size=24, family="Arial, sans-serif"),
        x=0.5,  # center the title horizontally
        xanchor='center',
        yanchor='top'
    ),
    font=dict(
        size=14,            # base font size for labels and hover
        family="Arial, sans-serif",
        color="#333"
    ),
    uniformtext=dict(
        minsize=12,         # minimum font size inside icicle blocks
        mode='show'         # force show all text (try 'hide' to remove overflow)
    ),
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_family="Arial, sans-serif"
    ),
    margin=dict(t=80, l=50, r=50, b=50),  # some padding around plot
)

    # Save the figure to an HTML file
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "icicle_chart.html")
    fig.write_html(output_file, include_plotlyjs='cdn')
    print(f"Icicle chart saved to {output_file}")

if __name__ == "__main__":
    icicle_data = load_data()
    create_dashboard(icicle_data)
    print("Dashboard created successfully!")
