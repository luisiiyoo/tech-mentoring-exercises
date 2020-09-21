
import os
import pandas as pd
from typing import Dict, List

FILES_EXTENSION = '.tsv'
PATH_DATA = './data/Dec2019-Mar2020/MENU/'
OUTPUT_PATH = './data_output/MENU/'

NUM_DAYS_SERVICE = 5
NO_SERVICE_TAGS = ['labor day', 'no service', 'holiday']


class MenuDBGenerator:
    def __init__(self, directory: str, extension: str, catering_col_idx=0, diet_col_idx=1):
        self.catering_col_idx = catering_col_idx
        self.diet_col_idx = diet_col_idx
        self.path = directory
        self.source_files = [
            file for file in os.listdir(self.path) if (file.endswith(extension))]

    def build(self, output_path: str, caterings: List[str] = ['Breakfast']) -> None:
        for catering in caterings:
            full_records_catering: List[Dict[str, str]] = []
            for files in self.source_files:
                df = self.readFile(files)
                records = self.generateRecordsByCatering(df, catering)
                full_records_catering = full_records_catering + records
            df_catering_sorted = self.transformData2DFIndexedByDate(
                full_records_catering)
            print(df_catering_sorted.head())

            ini_date, end_date = df_catering_sorted.index[[0, -1]]
            print(ini_date, end_date)
            print(f'MENU_{catering}({ini_date}_{end_date})')

            output_file_name = f'MENU_{catering}({ini_date}_{end_date})'
            self.saveDataFrameToCSV(
                df_catering_sorted, output_file_name, output_path)

    def transformData2DFIndexedByDate(self, data: List[Dict[str, str]], date_col_name: str = 'Date') -> pd.DataFrame:
        df = pd.DataFrame(data)
        # Converting "Date" column to date type
        df[date_col_name] = pd.to_datetime(
            df[date_col_name])  # format="%m/%d/%y"
        df[date_col_name] = df[date_col_name].dt.date
        # Sort by "Date" column
        df = df.sort_values(by=[date_col_name], ascending=True)
        # Set Date as index
        df = df.set_index(date_col_name)
        return df

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

    def readFile(self, file_name: str, separator: str = "\t") -> pd.DataFrame:
        full_path_file = self.path + file_name
        df = pd.read_csv(full_path_file, sep=separator)
        return df

    def getIndexOfSimilarValues(self, df: pd.DataFrame, col_name_idx: int, val: str) -> List[int]:
        return df.index[df.iloc[:, col_name_idx] == val].tolist()

    def generateRecordsByCatering(self, df: pd.DataFrame, catering: str) -> List[Dict[str, str]]:
        days_columns = df.columns[-NUM_DAYS_SERVICE:].tolist()
        catering_idxs = self.getIndexOfSimilarValues(
            df, self.catering_col_idx, catering)

        records: List[Dict[str, str]] = []
        for day_column in days_columns:
            record: Dict[str, str] = dict()
            record['Date'] = df.loc[0, day_column]
            record['Day'] = day_column.lower()
            # record['Temperature']

            for row_idx in catering_idxs:
                diet = df.iloc[row_idx, self.diet_col_idx].strip()
                dish = df.loc[row_idx, day_column].strip().lower()

                #
                dish = dish.replace('*', '').replace(' or ', ';')

                record['ServiceDay'] = dish not in NO_SERVICE_TAGS
                record[diet] = dish if (record['ServiceDay']) else None
            records.append(record)
        return records


# %% Main
generator = MenuDBGenerator(PATH_DATA, FILES_EXTENSION)
generator.build(OUTPUT_PATH, ['Breakfast', 'Lunch'])
