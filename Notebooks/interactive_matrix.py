import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from bkheatmap import bkheatmap
from bokeh.plotting import figure, output_file, show

output_file("output.html")
df = pd.read_csv("../Data/Cleaned_2019_2020_Players/outfield_players.csv", index_col=[1]).drop(columns=["1/3"])
header_df = pd.read_csv("../Data/Cleaned_2019_2020_Players/player_0_new_head.csv")

header = list(header_df.columns)
header.remove("Tackles + Interceptions")

df.columns = header

# fill all nan with zeros
df_zeroed = df.fillna(0)
print(df_zeroed.iloc[:, 11:])

# header.remove("row")
x = bkheatmap(df_zeroed.iloc[:, 12:14], prefix=header[12:14], scale="column")

show(x)
