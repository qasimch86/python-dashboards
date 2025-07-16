import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import os
# Change directory to Task3
BASE_DIR = os.path.dirname(os.path.abspath(__file__))# Load data

customer_df = pd.read_csv(os.path.join(BASE_DIR, "fake_customer_details.csv"))
map_df = pd.read_csv(os.path.join(BASE_DIR, "fake_map_data.csv"))
sales_df = pd.read_csv(os.path.join(BASE_DIR, "fake_monthly_sales.csv"))
gauge_df = pd.read_csv(os.path.join(BASE_DIR, "fake_sales_comparison.csv"))

# Summary data calculation
registered_users = len(customer_df)
weekly_visitors = int(registered_users * 0.65)  # Approximation or customize
subscriptions = len(customer_df[customer_df["Status"] == "Active"])
# Total orders read from orders CSV if needed
orders_df = pd.read_csv(os.path.join(BASE_DIR, "fake_orders.csv"))
total_orders = len(orders_df)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Subscription Dashboard"

# Map figure
fig_map = px.choropleth(
    map_df,
    locations="Country",
    locationmode="country names",
    color="Users",
    color_continuous_scale="Blues",
    title="User Distribution by Country"
)

fig_map.update_layout(
    height=800,
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth',
        fitbounds="locations"  # Zooms to the locations in your data
    )
)

# Monthly sales bar chart
fig_sales = px.bar(
    sales_df,
    x="Month",
    y=["Product A", "Product B"],
    barmode="group",
    title="Monthly Sales by Product"
)

# Sales index bar chart (gauge alternative)
fig_gauge = px.bar(
    gauge_df,
    x="Country",
    y="Sales Index",
    title="Sales Index by Country",
    color="Sales Index",
    color_continuous_scale="Viridis"
)

# Layout
app.layout = html.Div(style={"fontFamily": "Arial, sans-serif", "margin": "10px"}, children=[
    html.H1("Subscription Dashboard", style={"textAlign": "center"}),

    # Summary tiles
    html.Div(style={"display": "flex", "justifyContent": "space-around", "marginBottom": "30px"}, children=[
        html.Div([
            html.H3("Registered Users"),
            html.P(f"{registered_users}", style={"fontSize": "24px", "fontWeight": "bold"})
        ], style={"padding": "20px", "border": "1px solid #ddd", "borderRadius": "8px", "width": "20%"}),

        html.Div([
            html.H3("Weekly Visitors"),
            html.P(f"{weekly_visitors}", style={"fontSize": "24px", "fontWeight": "bold"})
        ], style={"padding": "20px", "border": "1px solid #ddd", "borderRadius": "8px", "width": "20%"}),

        html.Div([
            html.H3("Subscriptions"),
            html.P(f"{subscriptions}", style={"fontSize": "24px", "fontWeight": "bold"})
        ], style={"padding": "20px", "border": "1px solid #ddd", "borderRadius": "8px", "width": "20%"}),

        html.Div([
            html.H3("Total Orders"),
            html.P(f"{total_orders}", style={"fontSize": "24px", "fontWeight": "bold"})
        ], style={"padding": "20px", "border": "1px solid #ddd", "borderRadius": "8px", "width": "20%"}),
    ]),

    # Map (full width)
    html.Div([
    dcc.Graph(figure=fig_map, config={"responsive": True})
], style={
    "width": "100%",
    "padding": "10px",
    "boxSizing": "border-box"
}),

    # Row with two charts side-by-side
    html.Div(style={"display": "flex", "gap": "20px"}, children=[

        html.Div([
            dcc.Graph(figure=fig_sales)
        ], style={"flex": "1", "border": "1px solid #ddd", "borderRadius": "8px", "padding": "10px"}),

        html.Div([
            dcc.Graph(figure=fig_gauge)
        ], style={"flex": "1", "border": "1px solid #ddd", "borderRadius": "8px", "padding": "10px"})
    ])
])


if __name__ == "__main__":
    app.run_server(debug=True)
