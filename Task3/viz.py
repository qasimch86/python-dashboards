import pandas as pd
import plotly.express as px
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load data
customer_df = pd.read_csv(os.path.join(BASE_DIR, "fake_customer_details.csv"))
map_df = pd.read_csv(os.path.join(BASE_DIR, "fake_map_data.csv"))
sales_df = pd.read_csv(os.path.join(BASE_DIR, "fake_monthly_sales.csv"))
gauge_df = pd.read_csv(os.path.join(BASE_DIR, "fake_sales_comparison.csv"))
orders_df = pd.read_csv(os.path.join(BASE_DIR, "fake_orders.csv"))

# Summary calculations
registered_users = len(customer_df)
weekly_visitors = int(registered_users * 0.65)
subscriptions = len(customer_df[customer_df["Status"] == "Active"])
total_orders = len(orders_df)

# Create figures
fig_map = px.choropleth(
    map_df,
    locations="Country",
    locationmode="country names",
    color="Users",
    color_continuous_scale="Blues",
    title="User Distribution by Country"
)
fig_map.update_layout(height=600, margin={"r":0,"t":50,"l":0,"b":0}, geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'))

fig_sales = px.bar(
    sales_df,
    x="Month",
    y=["Product A", "Product B"],
    barmode="group",
    title="Monthly Sales by Product"
)

fig_gauge = px.bar(
    gauge_df,
    x="Country",
    y="Sales Index",
    color="Sales Index",
    color_continuous_scale="Viridis",
    title="Sales Index by Country"
)

# Generate individual divs for the figures (include_plotlyjs='cdn' only once)
map_html = fig_map.to_html(full_html=False, include_plotlyjs='cdn')
sales_html = fig_sales.to_html(full_html=False, include_plotlyjs=False)
gauge_html = fig_gauge.to_html(full_html=False, include_plotlyjs=False)

# Build summary HTML cards
summary_cards_html = f"""
<div style="display:flex; justify-content:space-around; margin-bottom:30px;">
    <div style="padding:20px; border:1px solid #ddd; border-radius:8px; width:20%; text-align:center;">
        <h3>Registered Users</h3>
        <p style="font-size:24px; font-weight:bold;">{registered_users}</p>
    </div>
    <div style="padding:20px; border:1px solid #ddd; border-radius:8px; width:20%; text-align:center;">
        <h3>Weekly Visitors</h3>
        <p style="font-size:24px; font-weight:bold;">{weekly_visitors}</p>
    </div>
    <div style="padding:20px; border:1px solid #ddd; border-radius:8px; width:20%; text-align:center;">
        <h3>Subscriptions</h3>
        <p style="font-size:24px; font-weight:bold;">{subscriptions}</p>
    </div>
    <div style="padding:20px; border:1px solid #ddd; border-radius:8px; width:20%; text-align:center;">
        <h3>Total Orders</h3>
        <p style="font-size:24px; font-weight:bold;">{total_orders}</p>
    </div>
</div>
"""

# Compose full HTML dashboard page
full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Subscription Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 10px; }}
        h1 {{ text-align: center; }}
        .row {{
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }}
        .flex-1 {{
            flex: 1;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
        }}
    </style>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>Subscription Dashboard</h1>
    {summary_cards_html}

    <div style="margin-bottom: 40px;">
        {map_html}
    </div>

    <div class="row">
        <div class="flex-1">{sales_html}</div>
        <div class="flex-1">{gauge_html}</div>
    </div>
</body>
</html>
"""

# Save to file
output_path = os.path.join(BASE_DIR, "dashboard_static.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"✅ Static dashboard saved at {output_path}")
