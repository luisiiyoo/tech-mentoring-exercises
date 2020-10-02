import pandas
from termcolor import colored, cprint
from typing import List, Dict, Set, Tuple, Union
import pickle
from Util import Color, DIETS
from BagOfWords import BagOfWords
import os


class GroupData:
    '''
    GroupData class to create a new data set that merge the information about Registers, Menus and BagOfWords instance previously obtained

    Args:
        path_file_registers (str): File that contains the data about registers
        path_file_menu (str): File that contains the data about menus
        bow_file_path (str): File that contains the instance of BagOfWords 

    Attributes:
        df_registers (pandas.DataFrame): Data frame that contains the records about registers
        df_menu (pandas.DataFrame): Data frame that contains the records about menus
        bow (BagOfWords): BagOfWords instance previously obtained
        common_dates (): Dates that match between df_registers and df_menu
        different_dates (): Dates that don't match between df_registers and df_menu
        group_data (List[Dict[str, Union[str, int]]]): List of dictionaries that contains the grouped records
    '''

    def __init__(self, path_file_registers: str, path_file_menu: str, bow_file_path: str):
        df_registers = pandas.read_csv(path_file_registers, index_col=0)
        self.df_registers = df_registers.fillna('')

        filter_col_name_menu = 'ServiceDay'
        df_menu = pandas.read_csv(path_file_menu)
        df_menu = df_menu.loc[df_menu[filter_col_name_menu], :]
        self.df_menu = df_menu.reset_index(drop=True)

        self.bow = self.__loadFile(bow_file_path)
        self.common_dates: List[str] = []
        self.different_dates: List[str] = []
        self.group_data: List[Dict[str, Union[str, int]]] = []

        diets_registers = self.df_registers['Diet'].unique()
        cprint(f'\n{df_registers.head()}\n', 'cyan')
        cprint(f'{df_menu.head()}\n', 'magenta')
        cprint(f'\n{diets_registers}', 'red')
        cprint(f'\n{self.bow.getFeatures()}', 'blue')
        cprint(f'\n{self.bow.getFeaturesStemmedWordsDict()}', 'green')

    def __getCommonDates(self, date_col_name: str) -> Tuple[List[str], List[str]]:
        '''
        Gets the common dates between Registers and Menu data frames

        Args:
            date_col_name (str): Column name that refers to dates in both data frames

        Returns:
            common_dates (List[str]): List of strings in common between Registers and Menu data frames
            different_dates (List[str]): List of different strings between Registers and Menu data frames
        '''
        registers_unique_dates: Set = set(
            self.df_registers[date_col_name].unique())
        menu_unique_dates: Set = set(self.df_menu[date_col_name].unique())

        common_dates: Set = registers_unique_dates.intersection(
            menu_unique_dates)
        all_dates: Set = registers_unique_dates.union(menu_unique_dates)
        different_dates: Set = all_dates - common_dates
        return (list(common_dates), list(different_dates))

    def __loadFile(self, file_path: str) -> BagOfWords:
        '''
        Loads the BagOfWords instance

        Args:
            file_path (str): Path where is located the file

        Returns:
            bow (BagOfWords): BagOfWords instance
        '''
        bow: BagOfWords = None
        with open(file_path, 'rb') as f:
            bow = pickle.load(f)
        return bow

    def __getDataSatisfyCondition(self, df: pandas.DataFrame, col_name: str, value: Union[str, bool]) -> pandas.DataFrame:
        '''
        Gets records with a specific value in a column

        Args:
            df (pandas.DataFrame): Data
            col_name (str): Column name to filter data
            value (Union[str, bool]): Value to match into the data frame and get the records

        Returns:
            df_value (pandas.DataFrame): Data frame that contains the filtred records
        '''
        return df.loc[df[col_name] == value, :]

    def build(self) -> None:
        '''
        Groups the data to generate a new frame

        Args:
            None

        Returns:
            None
        '''
        self.common_dates, self.different_dates = self.__getCommonDates('Date')
        bow_features: List[str] = self.bow.getFeatures()
        cprint(
            f'Common dates: {len(self.common_dates)}. Dates not included: {len(self.different_dates)}', 'yellow')

        for indx, date in enumerate(self.common_dates):
            menu: pandas.DataFrame = self.__getDataSatisfyCondition(
                self.df_menu, 'Date', date)
            registers: pandas.DataFrame = self.__getDataSatisfyCondition(
                self.df_registers, 'Date', date)
            no_request = self.__getDataSatisfyCondition(
                registers, 'Request', False)
            request = self.__getDataSatisfyCondition(
                registers, 'Request', True)
            attend_request = self.__getDataSatisfyCondition(
                request, 'Attend', True)
            no_attend_request = self.__getDataSatisfyCondition(
                request, 'Attend', False)

            print('---'*20)
            print(f'[{indx}] Date: {date}', ' - ',
                  colored(f'Num. registers: {len(registers)}', Color.REGISTERS))
            print(colored(f'Request: {len(request)}', Color.REQUEST), ' - ',
                  colored(f'No Request: {len(no_request)}', Color.NO_REQUEST))
            print(colored(f'Request & Attend: {len(attend_request)}', Color.ATTEND_REQUEST), ' - ',
                  colored(f'Request & No Attend: {len(no_attend_request)}', Color.NO_ATTEND_REQUEST))
            print('...'*20)
            for diet in DIETS:
                diet_request = len(self.__getDataSatisfyCondition(
                    request, 'Diet', diet))
                diet_attend_request = len(self.__getDataSatisfyCondition(
                    attend_request, 'Diet', diet))

                raw_text: List[str] = menu[diet].values
                bow_vector: List[int] = self.bow.vectorizeRawData(raw_text)[0]
                bow_dict = dict(zip(bow_features, bow_vector))

                group_record: Dict[str, Union[str, int]] = dict()
                group_record['Date'] = date
                group_record['Day'] = menu['Day'].values[0]
                group_record['Diet'] = diet
                group_record['TotalPeople'] = len(registers)
                group_record['TotalRequests'] = len(request)
                group_record['Request'] = diet_request
                group_record['Attend'] = diet_attend_request
                self.group_data.append({**bow_dict, **group_record})

    def saveDataFrameToCSV(self, full_path_file: str) -> None:
        '''
        Saves the grouped data

        Args:
            full_path_file (str): Complete path and file name where will be saved the file

        Returns:
            None
        '''
        output_path, output_file = os.path.split(full_path_file)
        if output_path and not os.path.isdir(output_path):
            try:
                os.makedirs(output_path)  # os.mkdir for one directory only
            except OSError:
                print("Creation of the directory %s failed" % output_path)
            else:
                print("Successfully created the directory %s " % output_path)
        print(f'Creating {output_file} file ...', end=' ')
        df = pandas.DataFrame(self.group_data)
        df['Date'] = pandas.to_datetime(df['Date'])
        df = df.sort_values(by=['Date'], ascending=True)
        df = df.reset_index(drop=True)
        df.to_csv(full_path_file)
        print('done')
