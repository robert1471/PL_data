import pandas as pd


def clean_players(play_num):
    test_file = pd.ExcelFile(f"../Notebooks/player_{play_num}.xlsx")

    sheet_dicts = {}
    for sheet in test_file.sheet_names:
        sheet_dicts[sheet] = pd.read_excel(f"../Notebooks/player_{play_num}.xlsx", sheet, header=1)
        # drop empty rows
        sheet_dicts[sheet] = sheet_dicts[sheet][sheet_dicts[sheet].Date.notnull()]
        # drop any repeated header lines
        sheet_dicts[sheet] = sheet_dicts[sheet].drop(sheet_dicts[sheet][sheet_dicts[sheet].Date == "Date"].index)

    master_df = pd.DataFrame()
    for i, sheet in enumerate(sheet_dicts):
        if i == 0:
            master_df = sheet_dicts[sheet]
        else:
            master_df = pd.concat([master_df, sheet_dicts[sheet]], axis=1)

    # reset index
    master_df.reset_index()

    # drop duplicates
    master_df = master_df.loc[:, ~master_df.columns.duplicated()]
    # drop empty rows
    master_df = master_df[master_df.Date.notnull()]
    # drop match report column
    master_df = master_df.drop("Match Report", axis=1)
    # change did not play to empty cell
    master_df = master_df.replace("On matchday squad, but did not play", "")
    # drop extra index column
    master_df = master_df.drop("Unnamed: 0", 1)

    master_df.to_csv(f"../Data/Cleaned_2019_2020_Players/player_{play_num}.csv")


for i in range(197, 600):
    clean_players(i)
