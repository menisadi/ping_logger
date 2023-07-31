import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

data = pd.read_csv("pings.csv")

# Convert the time column to datetime
data["time"] = pd.to_datetime(data["time"])

# consider only data from 7am to 23pm
data = data[(data["time"].dt.hour >= 7) & (data["time"].dt.hour <= 23)]
# consider only data from Sunday to Thursday
data = data[
    (data["time"].dt.dayofweek <= 3) | (data["time"].dt.dayofweek == 6)
]

bad_pings = data[data["delay"] == float("inf")]
good_pings = data[data["delay"] != float("inf")]

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
    {
        "href": "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Create a header container
header_container = html.Div(
    [
        html.H1(children="Ping statistics", className="header-title"),
        dcc.DatePickerRange(
            id="date-range",
            display_format="YYYY-MM-DD",
            start_date=data["time"].min(),
            end_date=data["time"].max(),
            className="daterangepicker",
        ),
    ],
    className="header-container",
)


# Define callback to update the graphs based on the selected date range
@app.callback(
    [
        Output("ping-delays", "figure"),
        Output("median-delay-per-hour", "figure"),
        Output("median-delay-per-day-hour", "figure"),
    ],
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_graphs(start_date, end_date):
    filtered_data = data.loc[
        (data["time"] >= start_date) & (data["time"] <= end_date)
    ]

    # Update figures using the filtered data
    ping_delays_figure = {
        "data": [
            {
                "x": filtered_data[filtered_data["delay"] != float("inf")][
                    "time"
                ],
                "y": filtered_data[filtered_data["delay"] != float("inf")][
                    "delay"
                ],
                "type": "scatter",
                "mode": "markers",
                "name": "Good pings",
            },
            {
                "x": filtered_data[filtered_data["delay"] == float("inf")][
                    "time"
                ],
                "y": [5]
                * len(filtered_data[filtered_data["delay"] == float("inf")]),
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
    }

    median_delay_per_hour_figure = {
        "data": [
            {
                "x": filtered_data["time"].dt.hour,
                "y": filtered_data["delay"],
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
    }

    median_delay_per_day_hour_figure = {
        "data": [
            {
                "x": filtered_data["time"].dt.dayofweek,
                "y": filtered_data["time"].dt.hour,
                "z": filtered_data["delay"],
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
    }

    figures = [
        ping_delays_figure,
        median_delay_per_hour_figure,
        median_delay_per_day_hour_figure,
    ]
    return figures


app.layout = html.Div(
    [
        # Use the header_container here
        header_container,
        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            children="Ping delays", className="card-title"
                        ),
                        dcc.Graph(
                            id="ping-delays",
                            figure={},
                        ),
                    ],
                    className="card",
                ),
                html.Div(
                    [
                        html.H2(
                            "Median delay per hour", className="card-title"
                        ),
                        dcc.Graph(
                            id="median-delay-per-hour",
                            figure={},
                        ),
                    ],
                    className="card",
                ),
                html.Div(
                    [
                        html.H2(
                            "Median delay: "
                            "per day of the week and hour of the day",
                            className="card-title",
                        ),
                        dcc.Graph(
                            id="median-delay-per-day-hour",
                            figure={},
                        ),
                    ],
                    className="card",
                ),
            ],
            className="graphs-container",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server()
