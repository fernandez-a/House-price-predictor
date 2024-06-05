import pandas as pd
import numpy as np


def rename_uname(df):
    for i , columns in enumerate(df.columns.levels):
        column_new = columns.tolist()
        for j, row in enumerate(column_new):
            if 'Unnamed' in row:
                column_new[j] = ""
            if "NO" == row:
                column_new = ""
        df = df.rename(columns=dict(zip(columns.tolist(), column_new)),
            level = i)
    return df


xls = pd.ExcelFile('../data/madrid/cleaned/population_total.xlsx')
sheets = xls.sheet_names
for i in range(len(sheets)):
    sheet = pd.read_excel('../data/madrid/cleaned/population_total.xlsx',header=[1,2], skiprows=3, sheet_name=i)

    sheet = sheet.drop([0,1,2])
    sheet = sheet.drop(sheet.columns[[0,1]], axis=1)
    sheet = sheet.iloc[:-3]

    sheet = rename_uname(sheet)
    sheet.columns = [' '.join(col).strip() for col in sheet.columns.values]
    sheet.columns = [col.replace(' ','_').lower() for col in sheet.columns.values]
    sheet = sheet.drop(sheet.columns[0], axis=1)
    sheet = sheet.loc[:, ~sheet.columns.str.endswith('.1')]

    sheet.to_csv(f"../data/madrid/raw/population/population_total_{sheets[i].split(' ')[-1]}.csv", index=False)
