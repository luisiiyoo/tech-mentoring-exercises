
import os
import pandas as pd
from typing import List


PATH_DATA = './data/'
FILE_NAME = PATH_DATA+'Copy of April Menu 2019.xlsx'
OUTPUT_PATH = './data_output/'
OUTPUT_BREAKFAST_FILE = OUTPUT_PATH + 'foodie_breakfast.csv'
OUTPUT_LUNCH_FILE = OUTPUT_PATH + 'foodie_lunch.csv'


def getIndxEmptyData(df, idxCol):
    return df.index[df.iloc[:, idxCol].isnull()].tolist()


def getDataCateringRanges(df: pd.DataFrame, idx_col: int, start_row_id: int = 2):
    idxs_delimiters = getIndxEmptyData(df, idx_col) + [len(df.index)]

    ranges = dict()
    for idx_delimiter in idxs_delimiters:
        catering = df.loc[start_row_id, 'Catering'].lower()
        if (catering == 'lunch'):
            ranges[catering] = range(start_row_id, idx_delimiter-1, 2)
        else:
            ranges[catering] = range(start_row_id, idx_delimiter, 1)
        start_row_id = idx_delimiter + 1
    return ranges


def getRecord(df: pd.DataFrame, date: str, day: str, breakfast_range: range, col_idxs: list):
    diet_key_idx_col, diet_descr_idx_col = col_idxs

    record = dict()
    record['Date'] = date
    record['Day'] = day
    for idx in breakfast_range:
        diet_key = df.iloc[idx, diet_key_idx_col].replace(' ', '')
        diet_descr = df.iloc[idx, diet_descr_idx_col].strip().lower()

        # key: Diet , value: row diet description
        if(diet_descr != 'labor day'):
            record['ServiceDay'] = True
            record[diet_key] = diet_descr
        else:
            record['ServiceDay'] = False
            record[diet_key] = None
    return record


def conver2DataFrame(data: list, idxColName):
    df = pd.DataFrame(data)
    df[idxColName] = pd.to_datetime(
        df[idxColName], format="%m/%d/%y")
    df[idxColName] = df[idxColName].dt.date
    # %% set index
    df = df.set_index(idxColName)
    return df


def transformData(sheets, file_name, date_column_idx=2, num_days_service=5):
    breakfast_data = list()
    lunch_data = list()
    for sheet in sheets[:]:
        df = pd.read_excel(file_name, sheet_name=sheet)
        # Removing the dates row (they will be used as a index)
        dates_sheet = df.iloc[0, -num_days_service:]

        catering_ranges = getDataCateringRanges(df, date_column_idx)
        print(catering_ranges)

        for idx_col in range(date_column_idx, len(df.columns)):
            date_idx = idx_col - date_column_idx
            date = dates_sheet[date_idx]
            day = dates_sheet.index[date_idx].lower()

            idx_cols_dish = [1, idx_col]
            # Get Record for Breakfast
            breakfast_record = getRecord(
                df, date, day, catering_ranges['breakfast'], idx_cols_dish)
            breakfast_data.append(breakfast_record)

            # Get Record for Lunch
            lunch_record = getRecord(
                df, date, day, catering_ranges['lunch'], idx_cols_dish)
            lunch_data.append(lunch_record)

    df_breakfast = conver2DataFrame(breakfast_data, 'Date')
    df_lunch = conver2DataFrame(lunch_data, 'Date')
    return df_breakfast, df_lunch


# %% Read data sheets
xls = pd.ExcelFile(FILE_NAME)
sheets = xls.sheet_names

# %% Get trasnform data
df_breakfast, df_lunch = transformData(sheets, FILE_NAME)

# print(df_breakfast)
# print(df_lunch)
# print(df_breakfast.shape)

# %% Save Files
print('\n')
if not os.path.isdir(OUTPUT_PATH):
    try:
        os.mkdir(OUTPUT_PATH)
    except OSError:
        print("Creation of the directory %s failed" % OUTPUT_PATH)
    else:
        print("Successfully created the directory %s " % OUTPUT_PATH)
print('Creating breakfast data ...', end=' ')
df_breakfast.to_csv(OUTPUT_BREAKFAST_FILE)
print('done')
print('Creating lunch data ...', end=' ')
df_lunch.to_csv(OUTPUT_LUNCH_FILE)
print('done')
