import pandas as pd

with open('pinger.log', 'r') as f:
    logf = f.readlines()

data_lines = [(logf[i-2], logf[i])
              for i, l in enumerate(logf)
              if l[3:8] == 'bytes']

data_lines = [(t[:-1], float(d.split()[-2][5:])) for t, d in data_lines]
df = pd.DataFrame(data_lines, columns=['time', 'delay'])

df['time'] = pd.to_datetime(df['time'],
                            dayfirst=True, format="%m/%d/%y-%H:%M:%S")
df.to_csv("pings.csv")

