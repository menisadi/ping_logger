import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Load data (replace 'pings.csv' with the path to your data file)
df = pd.read_csv("pings.csv")
df["time"] = pd.to_datetime(df["time"])
df["5"] = 5

# Calculate median delay for each hour of the day
df["hour"] = df["time"].dt.hour
median_delay_per_hour = (
    df[df["delay"] != np.inf].groupby("hour")["delay"].median().reset_index()
)

# Create Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div(
    [
        dcc.Graph(id="scatter-plot"),
        dcc.Graph(id="bar-plot"),
        dcc.Dropdown(
            id="log-scale-dropdown",
            options=[
                {"label": "Linear Scale", "value": "linear"},
                {"label": "Log Scale", "value": "log"},
            ],
            value="log",
            style={"width": "200px"},
        ),
    ]
)


# Define callbacks
@app.callback(
    Output("scatter-plot", "figure"),
    Output("bar-plot", "figure"),
    Input("log-scale-dropdown", "value"),
)
def update_plots(log_scale):
    # Create scatter plot for good and bad pings
    trace_good = px.scatter(
        df[df["delay"] != np.inf], x="time", y="delay", log_y=log_scale
    )
    trace_bad = px.scatter(df[df["delay"] == np.inf], x="time", y="5", log_y=log_scale)
    trace_bad.update_traces(marker=dict(color="red", symbol="x"))

    # Create bar plot for median delay per hour
    bar_trace = go.Bar(
        x=median_delay_per_hour["hour"],
        y=median_delay_per_hour["delay"],
        name="Median Delay",
    )

    # Create subplots
    scatter_plot = go.Figure(data=[trace_good.data[0], trace_bad.data[0]])
    bar_plot = go.Figure(data=[bar_trace])

    # Update layout and axis settings
    scatter_plot.update_layout(title_text="Scatter Plot - Pings Analysis")
    scatter_plot.update_layout(yaxis_type=log_scale)
    bar_plot.update_layout(title_text="Bar Plot - Median Delay per Hour")
    bar_plot.update_layout(yaxis_type=log_scale)

    return scatter_plot, bar_plot


if __name__ == "__main__":
    app.run_server(debug=True)
