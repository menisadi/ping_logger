import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

data = pd.read_csv("pings.csv")

# Convert the time column to datetime
data["time"] = pd.to_datetime(data["time"])

# consider only data from 7am to 23pm
data = data[(data["time"].dt.hour >= 7) & (data["time"].dt.hour <= 23)]
# consider only data from Sunday to Thursday
# data = data[
#     (data["time"].dt.dayofweek <= 3) | (data["time"].dt.dayofweek == 6)
# ]

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
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Ping statistics"

# Create a header container
header_container = html.Div(
    [
        html.P(
            children="📈",
            className="header-emoji",
        ),
        html.H1(children="Ping statistics", className="header-title"),
        html.P(
            children="Analyzing ping statistics of my internet connection",
            className="header-description",
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

    # keep only the "good" pings
    filtered_good_data = filtered_data[filtered_data["delay"] != float("inf")]

    # filter out Friday and Saturday from the data
    # filtered_data = filtered_data[
    #     (filtered_data["time"].dt.dayofweek <= 3)
    #     | (filtered_data["time"].dt.dayofweek == 6)
    # ]

    # Update figures using the filtered data

    # Calculate the median delay per hour
    median_delay_per_hour = (
        filtered_good_data.groupby(filtered_good_data["time"].dt.hour)["delay"]
        .median()
        .reset_index()
    )

    # Calculate the median delay per day of the week and hour of the day
    median_delay_per_day_hour = (
        filtered_good_data.groupby(
            [
                filtered_good_data["time"].dt.dayofweek,
                filtered_good_data["time"].dt.hour,
            ]
        )["delay"]
        .median()
        .reset_index(level=0)
        .rename(columns={"time": "dayofweek"})
        .reset_index()
        .rename(columns={"time": "hour"})
    )

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
                "x": median_delay_per_hour["time"],
                "y": median_delay_per_hour["delay"],
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
            {  # color is set to logarithmic scale of the delay
                "y": median_delay_per_day_hour["dayofweek"],
                "x": median_delay_per_day_hour["hour"],
                "z": median_delay_per_day_hour["delay"],
                "type": "heatmap",
                "coloraxis": "coloraxis",
                "colorscale": "Plotly3",
            },
        ],
        "layout": {
            "yaxis": {
                "title": "Day of the week",
                "tickmode": "array",
                "tickvals": [6, 0, 1, 2, 3, 4, 5],
                "ticktext": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
                "type": "category",
            },
            "xaxis": {
                "title": "Hour of the day",
                "dtick": 1,
                "tickformat": "%H",
            },
            "coloraxis": {
                "colorscale": "Plotly3",
                "colorbar": {
                    "title": "Median delay (log scale)",
                    "titleside": "right",
                },
            },
            "autosize": True,
            "aspectratio": 1,
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
                dcc.DatePickerRange(
                    id="date-range",
                    display_format="YYYY-MM-DD",
                    start_date=data["time"].min(),
                    end_date=data["time"].max(),
                    className="daterangepicker",
                ),
            ],
            className="date-range-container",
        ),
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
