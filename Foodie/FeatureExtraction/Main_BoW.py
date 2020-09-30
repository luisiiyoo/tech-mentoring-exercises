import pandas
from typing import List, Dict, Set
from termcolor import colored, cprint
from BagOfWords import BagOfWords
import time

MAX_FEATURES = 50
INPUT_FILES = ['./data_output/MENU/MENU_Breakfast(2019-12-30_2020-03-20).csv',
               './data_output/MENU/MENU_Lunch(2019-12-30_2020-03-20).csv']
OUTPUT_FILES = [f'./data_output/BoW/bow_breakfast_{MAX_FEATURES}_features.pkl',
                f'./data_output/BoW/bow_lunch_{MAX_FEATURES}_features.pkl']
COL_NAMES_DATA = ['Regular', 'Light', 'Vegan', 'Vegetarian']
FILTER_COL_NAME = 'ServiceDay'

for input_file, output_file in zip(INPUT_FILES, OUTPUT_FILES):
    df = pandas.read_csv(input_file, index_col=0)
    # print(df.head())
    # print(df.columns)
    # print()
    start = time.time()
    bow = BagOfWords(COL_NAMES_DATA, MAX_FEATURES)
    bow.build(df, FILTER_COL_NAME)
    bow.saveResults(output_file)
    # bow.vectorizeRawData(
    #     [' trivorced chilaquiles; egg tortilla; 1/2 portion of chilaquiles and 1/2 egg tortilla'])
    end = time.time()
    print(end - start)
