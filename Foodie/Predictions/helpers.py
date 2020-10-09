from pandas import DataFrame
from typing import List, Dict
from termcolor import cprint, COLORS
from regression import AbstractRegression, MultipleLinearRegression, SupportVectorRegression, PolynomialRegression, DecisionTreeRegression, RandomForestRegression


def build_model(models_names: List[str], x_train: DataFrame, x_valid: DataFrame, y_train: DataFrame, y_valid: DataFrame,
                max_cardinality: int = 10, estimators: List[int] = [250],
                svr_kernel: List[str] = ['rbf'], poly_degree: List[int] = [2],
                random_state: int = 0) -> Dict[str, AbstractRegression]:
    """
    Creates a dictionary based on a list of desired regression models

    Args:
        models_names (List[str]): List of regression models names.
        x_train (pandas.DataFrame): Independent variables from the training data.
        x_valid (pandas.DataFrame): Independent variables from the validation data.
        y_train (pandas.DataFrame): Dependent variable from the training data.
        y_valid (pandas.DataFrame): Dependent variable from the validation data.
        max_cardinality (int): Maximum cardinality to apply OneHotEncoder
        estimators (List[int]): List of estimators for Random Forest Regression
        svr_kernel (List[str]): Kernel list names for Support Vector Regression
        poly_degree (List[int]): List of degrees for  Polynomial Regression
        random_state (int): Number used for initializing the internal random number generator

    Returns:
        Dict[str, AbstractRegression]: Dictionary containing the models specified in the models_names list
    """
    model_dict: Dict[str, AbstractRegression] = dict()
    num_models = len(models_names)
    color_list = list(COLORS.keys())[1:]
    num_colors = len(color_list)
    circular_colors = [color_list[i % num_colors] for i in range(0, num_models)]

    for idx, model_name in enumerate(models_names):
        color = circular_colors[idx]
        if model_name == "MultipleLinearRegression":
            key_model = model_name
            model_dict[key_model] = MultipleLinearRegression(
                x_train, x_valid, y_train, y_valid, max_cardinality, print_color = color)
        elif model_name == "SupportVectorRegression":
            for kernel in svr_kernel:
                key_model = f'{model_name}_{kernel}Kernel'
                model_dict[key_model] = SupportVectorRegression(
                    x_train, x_valid, y_train, y_valid, max_cardinality, kernel = kernel, print_color= color)
        elif model_name == "PolynomialRegression":
            for degree in poly_degree:
                key_model = f'{model_name}_{degree}Degree'
                model_dict[key_model] = PolynomialRegression(
                    x_train, x_valid, y_train, y_valid, max_cardinality, degree = degree, print_color = color)
        elif model_name == "DecisionTreeRegression":
            key_model = model_name
            model_dict[key_model] = DecisionTreeRegression(
                x_train, x_valid, y_train, y_valid, max_cardinality, random_state = random_state, print_color = color)
        elif model_name == "RandomForestRegression":
            for num_estimators in estimators:
                key_model = f'{model_name}_{num_estimators}Estimators'
                model_dict[key_model] = RandomForestRegression(
                    x_train, x_valid, y_train, y_valid, max_cardinality, random_state = random_state, 
                    num_estimators = num_estimators, print_color = color)
    return model_dict


def evaluate_models(model_dict: Dict[str, AbstractRegression], num_folds: int = 10, scoring: str = 'r2') -> None:
    """
    Creates a dictionary based on a list of desired regression models

    Args:
        model_dict (Dict[str, AbstractRegression]): Dictionary containing the models specified in the models_names list
        num_folds (int): Number of cross validation folds
        scoring (str): Type of scoring evaluation

    Returns:
        None
    """
    for key in model_dict:
        model = model_dict[key]
        color = model._print_color
        r2_score = model.build_and_evaluate()
        r2_mean_train, r2_std_train = model.get_cross_validation_mean_score(
            num_folds, scoring)

        cprint(f'{key}', color)
        cprint(f'\tCrossVal R2 (Train):  mean: {r2_mean_train:.3f} ,  std: {r2_std_train:.3f}', color)
        cprint(f'\tR2 (Validation): {r2_score:.3f}', color)
    return
