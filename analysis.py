import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def read_log(file_name):
    """
    read the data
    """
    with open(file_name, "r") as f:
        logf = f.readlines()

    data_lines = [
        (logf[i - 1], logf[i + 1])
        for i, l in enumerate(logf)
        if l[:4] == "PING"
    ]

    def clean_delay(d):
        if d == "\n":
            return np.inf
        else:
            return float(d.split()[-2][5:])

    data_lines = [(t[:-1], clean_delay(d)) for t, d in data_lines]

    df = pd.DataFrame(data_lines, columns=["time", "delay"])

    return df


def fix_times(df):
    """
    Remove bad values from the time column
    """
    number_of_bad_times = 0

    for i, row in df.iterrows():
        temp = df["time"].iloc[i]
        try:
            pd.to_datetime(temp, dayfirst=True, format="%m/%d/%y-%H:%M:%S")
        except ValueError:
            number_of_bad_times += 1
            df.loc[i, "time"] = pd.to_datetime(0)

    df["time"] = pd.to_datetime(
        df["time"], dayfirst=True, format="%m/%d/%y-%H:%M:%S"
    )

    df = df[df["time"] != pd.to_datetime(0)]

    return df, number_of_bad_times


def plot_log_to_file(df):
    plt.figure(figsize=(12, 6))
    g = sns.scatterplot(data=df[df["delay"] != np.inf], x="time", y="delay")
    sns.scatterplot(
        data=df[df["delay"] == np.inf],
        x="time",
        y=5,
        style="delay",
        markers=["x"],
        hue="delay",
        palette=["red"],
        ax=g,
    )
    g.set(yscale="log")
    g.set(title="Ping")
    plt.legend([], [], frameon=False)
    plt.savefig("ping.png")


if __name__ == "__main__":
    df = read_log("pinger.log")
    df, bad_times = fix_times(df)
    print(f"Number of bad times: {bad_times}")
    # write data to csv file
    df.to_csv("pings.csv")
    plot_log_to_file(df)
