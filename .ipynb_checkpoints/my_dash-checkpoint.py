import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


df = pd.read_csv("pings.csv")

# Convert the time column to datetime
df["time"] = pd.to_datetime(df["time"])

# Add a column with constant value 5 for the time-out pings to be visible on the plot
df["5"] = 5

# Create scatter plot for good pings (delays that are not infinity)
trace_good = px.scatter(df[df["delay"] != np.inf], x="time", y="delay", log_y=True)

# Create scatter plot for bad pings (delays that are infinity)
trace_bad = px.scatter(df[df["delay"] == np.inf], x="time", y="5", log_y=True)
trace_bad.update_traces(marker=dict(color="red", symbol="x"))

# Calculate median delay for each hour of the day
df["hour"] = df["time"].dt.hour
median_delay_per_hour = df[df["delay"] != np.inf].groupby("hour")["delay"].median()

# Calculate median delay for each combination of day of the week and hour of the day
df["day_of_week"] = df["time"].dt.dayofweek
df_filtered = df[(df["delay"] != np.inf) & (~df["day_of_week"].isin([4, 5]))]
median_delay_per_day_hour = (
    df_filtered.groupby(["day_of_week", "hour"])["delay"].median().unstack()
)
# Shift the days to start from Sunday
median_delay_per_day_hour = median_delay_per_day_hour.reindex(
    [2, 3, 4, 5, 6, 7, 1], axis=0)
# exclude Friday and Saturday
median_delay_per_day_hour = median_delay_per_day_hour.iloc[:5, :]
# Create bar plot for median delay per hour

bar_trace = go.Bar(x=median_delay_per_hour.index, y=median_delay_per_hour.values)

# Create heatmap plot for median delay per day of the week and hour of the day
heatmap_trace = go.Heatmap(
    x=median_delay_per_day_hour.columns,
    y=[
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
    ],  # Exclude Friday and Saturday
    z=median_delay_per_day_hour.values,
    colorscale="Viridis",
)

# Create subplots with two rows and one column
fig = make_subplots(rows=3, cols=1, shared_xaxes=False, vertical_spacing=0.1)

# Add scatter plot and bar plot to the subplots
fig.add_trace(trace_good.data[0], row=1, col=1)
fig.add_trace(trace_bad.data[0], row=1, col=1)
fig.add_trace(bar_trace, row=2, col=1)
fig.add_trace(heatmap_trace, row=3, col=1)

# Update layout and axis settings
fig.update_layout(height=900, title_text="Ping Analysis Dashboard")
fig.update_layout(yaxis_type="log", yaxis2_type="log")
fig.update_yaxes(title_text="Ping Delay (log scale)", row=1, col=1)
fig.update_yaxes(title_text="Median Delay (log scale)", row=2, col=1)
fig.update_xaxes(title_text="Time", row=2, col=1)
fig.update_xaxes(title_text="Hour of the Day", row=2, col=1, dtick=1, tickformat="%H")
fig.update_yaxes(title_text="Day of Week", row=3, col=1, dtick=1, tick0=1)
fig.update_xaxes(title_text="Hour of the Day", row=3, col=1, dtick=1, tickformat="%H")
fig.update_traces(showlegend=False)

fig.show()
