
import pandas as pd
from typing import List


PATH_DATA = './data/'
FILE_NAME = PATH_DATA+'Copy of April Menu 2019.xlsx'

xls = pd.ExcelFile(FILE_NAME)
sheets = xls.sheet_names


def getCateringRanges(df, colDiet, colCatering):
    idx_null = df.index[df[colDiet].isnull()].tolist()
    idx_caterings_names = [idx+1 for idx in idx_null]
    caterings = df.loc[idx_caterings_names, colCatering].values
    print(idx_null)
    print(caterings)


def getIndxEmptyData(df, idxCol):
    return df.index[df.iloc[:, idxCol].isnull()].tolist()


def getDataCateringRanges(df: pd.DataFrame, idx_col: int, start_row_id: int = 2):
    idxs = getIndxEmptyData(df, idx_col) + [len(df.index)]

    ranges = dict()
    for idx in idxs:
        catering = df.loc[start_row_id, 'Catering'].lower()
        ranges[catering] = range(start_row_id, idx)
        start_row_id = idx + 1
    return ranges


day_column_idx = 2
data = list()
for sheet in sheets[:]:
    # print(sheet, '\n')
    df = pd.read_excel(FILE_NAME, sheet_name=sheet)
    dates_data = df.iloc[0, -5:]

    # df.drop(index=[0, 1], inplace=True)  # df.index[1]
    catering_ranges = getDataCateringRanges(df, day_column_idx)
    print(catering_ranges)

    for idx_col in range(day_column_idx, len(df.columns)):
        record = dict()
        date_idx = idx_col-day_column_idx
        record['Date'] = dates_data[date_idx]
        record['Day'] = dates_data.index[date_idx].lower()

        # print(record['Day'], record['Date'])
        df_sub = df.iloc[catering_ranges['breakfast'], [1, idx_col]]
        # print(f'{dates_data.index[date_idx]}\n', df_sub, '\n\n')
        for index, row in df_sub.iterrows():
            # print(row[0], row[-1],  '\n')
            record[row[0]] = row[-1]
        data.append(record)

# Creates DataFrame.
print('\n')
df_breakfast = pd.DataFrame(data)
df_breakfast['Date'] = pd.to_datetime(
    df_breakfast['Date'], format="%m/%d/%y")
df_breakfast['Date'] = df_breakfast['Date'].dt.date

# %% set index
df_breakfast = df_breakfast.set_index('Date')
print(df_breakfast)
print(df_breakfast.shape)
df_breakfast.to_csv('foodie_breakfast.csv')
