import plotly.graph_objects as go

# Define the data for the icicle chart
# labels: names of the nodes
# parents: parent of each node (empty string for root nodes)
# values: optional, numerical values for sizing or coloring
labels = ["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"]
parents = ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"]
values = [10, 8, 7, 5, 3, 6, 4, 2, 9] # Optional: for sizing or coloring

# Create the Icicle trace
fig = go.Figure(go.Icicle(
    labels=labels,
    parents=parents,
    values=values, # Include if you want to use values
    root_color="lightgrey" # Optional: color for the root node
))

# Update layout for better visualization
fig.update_layout(
    title_text="Basic Icicle Chart",
    margin=dict(t=50, l=0, r=0, b=0) # Adjust margins
)

# Show the plot
fig.show()