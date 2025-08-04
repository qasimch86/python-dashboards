import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import os
script_dir = os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"Script directory: {script_dir}")
# data_path = os.path.join(script_dir, "..", "..", "data", "state_population.csv")
# Load data
df = pd.read_csv("data/state_population.csv")
years = [str(y) for y in range(2010, 2021)]

# Total population over time (for line chart)
total_pop = df[years].sum().reset_index()
total_pop.columns = ["Year", "Population"]
total_pop["Year"] = total_pop["Year"].astype(int)

line_fig = px.line(total_pop, x="Year", y="Population", title="Population over time")
line_fig.update_layout(height=400, margin=dict(t=30, l=10, r=10, b=10))

# Choropleth map for 2016
map_fig = px.choropleth(
    df,
    locations="State",
    locationmode="USA-states",
    color="2016",
    scope="usa",
    color_continuous_scale="Viridis",
    title="Population 2016"
)
map_fig.update_layout(height=400, margin=dict(t=30, l=10, r=10, b=10))

# Top states by 2020
top_states = df.nlargest(7, "2020").copy()
top_states["%"] = top_states["2020"] / top_states["2020"].max() * 100
top_bar = go.Figure(go.Bar(
    x=top_states["%"],
    y=top_states["State"],
    orientation="h",
    text=top_states["2020"],
    marker_color="green"
))
top_bar.update_layout(title="Top States", height=400, margin=dict(t=30, l=10, r=10, b=10), yaxis=dict(autorange="reversed"))

# Bottom states by 2020
bottom_states = df.nsmallest(7, "2020").copy()
bottom_states["%"] = bottom_states["2020"] / top_states["2020"].max() * 100
bottom_bar = go.Figure(go.Bar(
    x=bottom_states["%"],
    y=bottom_states["State"],
    orientation="h",
    text=bottom_states["2020"],
    marker_color="lightgreen"
))
bottom_bar.update_layout(title="Bottom 7 States", height=380, margin=dict(t=30, l=10, r=10, b=10), yaxis=dict(autorange="reversed"))

# Gains/Losses card (Texas and Puerto Rico)
def format_gain_card(state_name):
    current = df[df["State"] == state_name]["2020"].values[0]
    previous = df[df["State"] == state_name]["2010"].values[0]
    diff = current - previous
    color = "success" if diff >= 0 else "danger"
    arrow = "▲" if diff >= 0 else "▼"
    diff_str = f"{arrow} {abs(diff)//1000:,} K"
    return dbc.Card([
        html.H4(state_name, className="card-title"),
        html.H2(f"{current/1e6:.1f} M"),
        html.P(diff_str, className=f"text-{color}")
    ], body=True, color="light", className="mb-2")

# Growth donut
df["Growth"] = (df["2020"] - df["2010"]) / df["2010"]
avg_growth = df["Growth"].mean()
above = (df["Growth"] > avg_growth).sum()
below = (df["Growth"] <= avg_growth).sum()
donut = px.pie(
    names=["Above", "Below"],
    values=[above, below],
    hole=0.6,
    color_discrete_sequence=["green", "brown"]
)
donut.update_layout(title="States Growth", height=380, showlegend=False, margin=dict(t=30, l=10, r=10, b=10))

# Heatmap
heatmap_data = df.set_index("State")[years].T
heatmap_data.index.name = "Year"
heatmap_fig = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale="Viridis"
))
heatmap_fig.update_layout(title="Heatmap", height=380, margin=dict(t=30, l=10, r=10, b=10))

# Dash App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "US Population"

app.layout = dbc.Container([
    html.H3("US Population", className="my-3"),

    # Row 1
dbc.Row([
    dbc.Col(
        dbc.Card(dbc.CardBody([dcc.Graph(figure=line_fig)]), className="mb-4 shadow-sm"), md=4
    ),
    dbc.Col(
        dbc.Card(dbc.CardBody([dcc.Graph(figure=map_fig)]), className="mb-4 shadow-sm"), md=4
    ),
    dbc.Col(
        dbc.Card(dbc.CardBody([dcc.Graph(figure=top_bar)]), className="mb-4 shadow-sm"), md=4
    ),
]),

# Row 2
dbc.Row([
    dbc.Col([
        dbc.Card(dbc.CardBody([format_gain_card("Texas")]), className="mb-2 shadow-sm"),
        dbc.Card(dbc.CardBody([format_gain_card("Puerto Rico")]), className="mb-2 shadow-sm")
    ], md=2),

    dbc.Col(
        dbc.Card(dbc.CardBody([dcc.Graph(figure=donut)]), className="mb-2 shadow-sm"), md=2
    ),

    dbc.Col(
        dbc.Card(dbc.CardBody([dcc.Graph(figure=heatmap_fig)]), className="mb-4 shadow-sm"), md=4
    ),

    dbc.Col(
        dbc.Card(dbc.CardBody([dcc.Graph(figure=bottom_bar)]), className="mb-4 shadow-sm"), md=4
    )
])

], fluid=True)

# Run app locally
if __name__ == "__main__":
    app.run(debug=True)
