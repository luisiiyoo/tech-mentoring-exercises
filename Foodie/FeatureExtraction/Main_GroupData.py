from GroupData import GroupData

FILE_REGISTERS = './data_output/REGISTERS/REGISTERS_Breakfast(2019-12-09_2020-03-13).csv'
FILE_MENU = './data_output/MENU/MENU_Breakfast(2019-12-30_2020-03-20).csv'
MAX_FEATURES = 50
FILE_BOW = f'./data_output/BoW/bow_breakfast_{MAX_FEATURES}_features.pkl'
OUTPUT_PATH_FILE = f'./data_output/foodie_menu_records_{MAX_FEATURES}_features.csv'

gdata = GroupData(FILE_REGISTERS, FILE_MENU, FILE_BOW)
gdata.build()
gdata.saveDataFrameToCSV(OUTPUT_PATH_FILE)
