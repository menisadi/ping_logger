import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv("pings.csv")

# convert the time column to datetime
df["time"] = pd.to_datetime(df["time"])
# keep only the last 3 days
# first create a datetime object for 3 days ago
three_days_ago = pd.to_datetime("now") - pd.Timedelta(days=1)
df = df[df["time"] > three_days_ago]

df["5"] = 5  # for the time-out pings to be visible on the plot
fig = go.Figure()

trace_good = px.scatter(df[df["delay"] != np.inf], x="time", y="delay", log_y=True)
trace_bad = px.scatter(df[df["delay"] == np.inf], x="time", y="5", log_y=True)
trace_bad.update_traces(marker=dict(color="red", symbol="x"))

fig.add_trace(trace_good.data[0])
fig.add_trace(trace_bad.data[0])
fig.update_layout(yaxis_type="log")

# fig.show()
fig.write_html("pings.html", include_plotlyjs=False)
