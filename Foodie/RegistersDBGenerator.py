import os
import pandas as pd
from typing import Dict, List

FILES_EXTENSION = '.xlsx'
PATH_DATA = './data/Dec2019-Mar2020/REGISTERS/'
OUTPUT_PATH = './data_output/REGISTERS/'

EXTRA_TAG = ' + Extras'


class RegistersDBGenerator:
    def __init__(self, directory: str, extension: str):
        self.path = directory
        self.breakfast_cols_idx = [0, 1, 2]
        self.lunch_cols_idx = [0, 4, 5]
        self.source_files = [
            file for file in os.listdir(self.path) if (file.endswith(extension))]

    def build(self, output_path: str) -> None:
        df_breakfast = self.extractData(self.breakfast_cols_idx, False)
        ini_date = df_breakfast['Date'].iloc[0].date()
        end_date = df_breakfast['Date'].iloc[-1].date()
        print('Dates:', ini_date, 'To', end_date)

        # Brekafast
        breakfast_file_name = f'REGISTERS_Breakfast({ini_date}_{end_date})'
        self.saveDataFrameToCSV(df_breakfast, breakfast_file_name, output_path)
        del(df_breakfast)

        # Lunch
        df_lunch = self.extractData(self.lunch_cols_idx, True)
        ini_date = df_lunch['Date'].iloc[0].date()
        end_date = df_lunch['Date'].iloc[-1].date()
        print('Dates:', ini_date, 'To', end_date)

        lunch_file_name = f'REGISTERS_Lunch({ini_date}_{end_date})'
        self.saveDataFrameToCSV(df_lunch, lunch_file_name, output_path)
        del(df_lunch)

    def extractData(self, cols_idx: List[int], checkExtra: bool) -> pd.DataFrame:
        frames: List[pd.DataFrame] = []
        for file_name in self.source_files:
            full_file_name = PATH_DATA + file_name
            xls = pd.ExcelFile(full_file_name)
            sheets = xls.sheet_names
            print(full_file_name)
            for sheet in sheets:
                # Use only the interested columns
                df = pd.read_excel(full_file_name, sheet_name=sheet)
                print(df.shape, sheet)
                # print(df.head())
                if ((df.iloc[0:5, 0] == 'HOLIDAY').sum() > 0):
                    print(df.head())
                    continue
                df = df.iloc[1:, cols_idx]

                # Rename the columns
                col_names_old = df.columns
                date_record = col_names_old[0]
                col_names_new = ['Wizeliner', 'Diet', 'Attend']
                col_names_dict = dict(zip(col_names_old, col_names_new))
                df = df.rename(columns=col_names_dict)

                # Converting to the correct data type
                df['Request'] = df.loc[:, 'Diet'].notnull().tolist()
                df['Date'] = date_record
                df['Date'] = pd.to_datetime(df['Date'])
                df['Attend'] = df['Attend'].astype('bool')

                # Keep data that is not empty on 'Wizeliner' column
                df = df[df['Wizeliner'].notna()]

                # Reset index
                df.reset_index(drop=True, inplace=True)
                df = df[['Wizeliner', 'Date', 'Request', 'Attend', 'Diet']]

                if(checkExtra):
                    df['Extra'] = df['Diet'].fillna(
                        '').str.contains(EXTRA_TAG, regex=False)
                    df['Diet'] = df['Diet'].map(lambda diet: str(
                        diet).replace(EXTRA_TAG, '').strip(), na_action=None)

                # Save a copy
                frames.append(df)

                # print(df)
                # print(df.dtypes)
                # self.getPeopleRequestAndNotAttend(df)
        df_breakfast = pd.concat(frames, ignore_index=True, axis=0)
        df_breakfast.sort_values(by=['Date'], ascending=True, inplace=True)
        return df_breakfast.reset_index(drop=True)

    def saveDataFrameToCSV(self, df: pd.DataFrame, output_file: str, output_path: str) -> None:
        if not os.path.isdir(output_path):
            try:
                os.makedirs(output_path)  # os.mkdir for one directory only
            except OSError:
                print("Creation of the directory %s failed" % output_path)
            else:
                print("Successfully created the directory %s " % output_path)
        print(f'Creating {output_file} file ...', end=' ')
        full_output_path = output_path + output_file+'.csv'
        df.to_csv(full_output_path)
        print('done')

    def getPeopleRequestAndNotAttend(self, df: pd.DataFrame):
        condition = (df['Request'] == True) & (df['Attend'] == False)
        idx_condition = df.index[condition].tolist()
        print(df.loc[idx_condition, 'Wizeliner'])


# %% Main
generator = RegistersDBGenerator(PATH_DATA, FILES_EXTENSION)
generator.build(OUTPUT_PATH)
