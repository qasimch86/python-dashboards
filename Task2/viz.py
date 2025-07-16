import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

# Load sunburst data
df = pd.read_csv("./Task2/sunburst_data.csv")

# Create sunburst figure
fig = px.sunburst(
    df,
    path=["Region", "Category", "Sub-Category"],
    values="Sales",
    title="Sales Breakdown by Region, Category, and Sub-Category",
    color="Region",
    color_discrete_sequence=px.colors.qualitative.Set3,
)
# Customize layout
fig.update_layout(
    width=1400,
    height=900,
)

#Export the figure to HTML
fig.write_html("./Task2/sunburst_chart.html")
print("Sunburst chart saved to Task2/sunburst_chart.html")

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Sunburst Sales Dashboard"

# App layout
app.layout = html.Div(
    children=[
        html.H1("Sunburst Sales Dashboard", style={"textAlign": "center", "color": "#0020be"}),
        dcc.Graph(figure=fig),
    ],
    style={
        "backgroundColor": "#FFFFFF",
        "padding": "10px",
        'display': 'flex',
        'flexDirection': 'column',        # stack items vertically
        'justify-content': 'center',
        'align-items': 'center',
        # 'height': '100vh',  # full viewport height
        'color': '#fff',  # text color
        'fontFamily': 'Arial, sans-serif',
        'fontSize': '16px',
        'maxWidth': '100%',  # max width for larger screens
    }
)

# Run the server
if __name__ == "__main__":
    app.run(debug=False, port=8050)
