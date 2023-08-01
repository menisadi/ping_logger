import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

data = pd.read_csv("pings.csv")

# Convert the time column to datetime
data["time"] = pd.to_datetime(data["time"])


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

app.layout = html.Div(
    [
        children=[
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.P(children="📈", className="header-emoji"),
                            html.H1(
                                children="Ping statistics", className="header-title"
                            ),
                            html.P(
                                children=(
                                    "Analyzing my ping statistics "
                                    "with this simple app."
                                ),
                                className="header-description",
                            ),
                        ],
                        className="header",
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children="Date Range",
                                className="menu-title"
                            ),
                            dcc.DatePickerRange(
                                id="date-range",
                                min_date_allowed=data["time"].min().date(),
                                max_date_allowed=data["time"].max().date(),
                                start_date=data["time"].min().date(),
                                end_date=data["time"].max().date(),
                            ),
                        ],
                        className="menu",
                    ),
                ],
                className="app-header",
                ),
            html.Div(
                [
                    html.Div(
                        children=dcc.Graph(
                            id='total-pings',
                        ),
                        className = "card",
                    ),
                    html.Div(
                        children=dcc.Graph(
                            id='hours-averages',
                        ),
                        className = "card",
                    ),
                    html.Div(
                        children=dcc.Graph(
                            id='days-heatmap',
                        ),
                        className = "card",
                    ),
                ],
                className="graphs-container",
            ),
        ],
    ],
)


@app.callback(
    Output("total-pings", "figure"),
    Output("hours-averages", "figure"),
    Output("days-heatmap", "figure"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)

def update_charts(start_date, end_date):
    filtered_data = data[
        (data["time"] >= start_date) & (data["time"] <= end_date)
    ]
    filtered_bad_pings = filtered_data[filtered_data["delay"] == float("inf")]
    filtered_good_pings = filtered_data[filtered_data["delay"] != float("inf")]
    
    # scatter plot
    total_pings = {
            "data": [
                {
                    "x": filtered_data["time"],
                    "y": filtered_data["delay"],
                    "type": "scatter",
                },
            ],
            "layout": {
                "title": {
                    "text": "Total pings",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": {"fixedrange": True},
                "colorway": ["#17B897"],
            },
        }

    # bar plot
    hours_averages = {
            "data": [
                {
                    "x": filtered_good_pings["time"].dt.hour,
                    "y": filtered_good_pings["delay"],
                    "type": "bar",
                },
            ],
            "layout": {
                "title": {
                    "text": "Average ping by hour",
                    "x": 0.05,
                    "xanchor": "left",
                },
                "xaxis": {"fixedrange": True},
                "yaxis": {"fixedrange": True},
                "colorway": ["#E12D39"],
            },
        }

if __name__ == "__main__":
    app.run_server()
