import pandas
from sklearn.model_selection import train_test_split
from helpers import build_model, evaluate_models

INPUT_FILE = './data/foodie_menu_records_50_features.csv'
TARGET_COLUMN = 'Attend'
EXCLUDE_COLS = ['Date'] # 'Date'
MODELS = ['MultipleLinearRegression', 'SupportVectorRegression', 'PolynomialRegression', 'DecisionTreeRegression', 'RandomForestRegression']
MODELS = ['MultipleLinearRegression','DecisionTreeRegression', 'RandomForestRegression']
TEST_SIZE_PROPORTION = 1 / 5

RANDOM_STATE = 0
MAX_CARDINALITY = 10
ESTIMATORS = [300]
SVR_KERNEL = ['rbf']
POLY_DEGREE = [2]
PRINT_COMPARISON = False

# Read the data
data = pandas.read_csv(INPUT_FILE, index_col = 0)

# Remove rows with missing target, separate target from predictors
data.dropna(axis=0, subset=[TARGET_COLUMN], inplace=True)
y = data[TARGET_COLUMN]
X = data.drop([TARGET_COLUMN, *EXCLUDE_COLS], axis=1)

# Break off validation set from training data
x_train, x_valid, y_train, y_valid = train_test_split(
    X, y, test_size=TEST_SIZE_PROPORTION, random_state=RANDOM_STATE)

# Build models defined
models_dict = build_model(model_names = MODELS, x_train = x_train, x_valid = x_valid, 
                y_train = y_train, y_valid = y_valid,
                max_cardinality = MAX_CARDINALITY, estimators = ESTIMATORS,
                svr_kernel = SVR_KERNEL, poly_degree = POLY_DEGREE,
                random_state = RANDOM_STATE, print_comparison = PRINT_COMPARISON)

# Evaluate models defined
evaluate_models(models_dict)
