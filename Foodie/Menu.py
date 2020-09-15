import pandas as pd

PATH_DATA = './data/'
FILE_NAME = PATH_DATA+'Copy of April Menu 2019.xlsx'

xls = pd.ExcelFile(FILE_NAME)
sheets = xls.sheet_names

start_row_idx = 1
day_column_idx = 3


def getCateringRanges(df, colDiet, colCatering):
    idx_null = df.index[df[colDiet].isnull()].tolist()
    idx_caterings_names = [idx+1 for idx in idx_null]
    caterings = df.loc[idx_caterings_names, colCatering].values
    print(idx_null)
    print(caterings)


for sheet in sheets[:1]:
    # print(sheet, '\n')
    df = pd.read_excel(FILE_NAME, sheet_name=sheet)
    df.drop(df.index[1], inplace=True)

    # print(df['Catering'][start_idx:])
    # print(df.iloc[start_row_idx:, [0, 1, 2]])
    # print(len(df.columns))
    # ----
    print(df['La Universal'])
    # print(df.index[df['La Universal'].isnull()].tolist() + [len(df.index)])
    # getCateringRanges(df, 'La Universal', 'Catering')

    # %% For work on dates rows

    # for idx_col in range(day_column_idx, len(df.columns)):
    #     df_sub = df.iloc[start_row_idx:, [0, 1, idx_col]]
    #     # print('\n', df.iloc[0, idx_col], ':\n', df_sub)
    #     data = dict()
    #     prev_catering = ''
    #     for index, row in df_sub.iterrows():
    #         data['date'] = df.iloc[0, idx_col]  # getThe Date
    #         catering = row['catering']
    #         if(pd.isnull(catering)):
    #             catering = prev_catering
    #         else:
    #             prev_catering = catering
    #         data['catering'] = catering
