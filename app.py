import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

data = pd.read_csv("pings.csv")

# Convert the time column to datetime
data["time"] = pd.to_datetime(data["time"])


bad_pings = data[data["delay"] == float("inf")]
good_pings = data[data["delay"] != float("inf")]

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Ping statistics"),
        html.Div(
            [
                html.Div(
                    [
                        html.H2("Ping delays"),
                        dcc.Graph(
                            id="ping-delays",
                            figure={
                                "data": [
                                    {
                                        "x": good_pings["time"],
                                        "y": good_pings["delay"],
                                        "type": "scatter",
                                        "mode": "markers",
                                        "name": "Good pings",
                                    },
                                    {
                                        "x": bad_pings["time"],
                                        "y": [5] * len(bad_pings),
                                        "type": "scatter",
                                        "mode": "markers",
                                        "name": "Bad pings",
                                        "marker": {
                                            "color": "red",
                                            "symbol": "x",
                                        },
                                    },
                                ],
                                "layout": {
                                    "xaxis": {
                                        "title": "Time",
                                    },
                                    "yaxis": {
                                        "title": "Ping delay (log scale)",
                                        "type": "log",
                                    },
                                },
                            },
                        ),
                    ],
                    className="six columns",
                ),
                html.Div(
                    [
                        html.H2("Median delay per hour"),
                        dcc.Graph(
                            id="median-delay-per-hour",
                            figure={
                                "data": [
                                    {
                                        "x": data["time"].dt.hour,
                                        "y": data["delay"],
                                        "type": "bar",
                                    },
                                ],
                                "layout": {
                                    "xaxis": {
                                        "title": "Hour of the day",
                                        "dtick": 1,
                                        "tickformat": "%H",
                                    },
                                    "yaxis": {
                                        "title": "Median delay (log scale)",
                                        "type": "log",
                                    },
                                },
                            },
                        ),
                    ],
                    className="six columns",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.H2(
                    "Median delay per day of the week and hour of the day"
                ),
                dcc.Graph(
                    id="median-delay-per-day-hour",
                    figure={
                        "data": [
                            {
                                "x": data["time"].dt.dayofweek,
                                "y": data["time"].dt.hour,
                                "z": data["delay"],
                                "type": "heatmap",
                                "colorscale": "Viridis",
                                "coloraxis": "coloraxis",
                            },
                        ],
                        "layout": {
                            "xaxis": {
                                "title": "Day of the week",
                                "dtick": 1,
                                "tickformat": "%a",
                            },
                            "yaxis": {
                                "title": "Hour of the day",
                                "dtick": 1,
                                "tickformat": "%H",
                            },
                            "coloraxis": {
                                "colorscale": "Viridis",
                                "colorbar": {
                                    "title": "Median delay (log scale)",
                                    "titleside": "right",
                                },
                            },
                        },
                    },
                ),
            ],
            className="row",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server()
