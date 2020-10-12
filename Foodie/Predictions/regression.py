import warnings
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from pandas import DataFrame
from termcolor import cprint
from typing import List, Tuple, Any
from preprocessing import Preprocessing


class AbstractRegression:
    """
    Regression parent class witch is the responsible of all the preprocess, fit, transform and predict processes

    Args:
       x_train (pandas.DataFrame): Training independent variables
       x_valid (pandas.DataFrame): Validation independent variables
       y_train (pandas.DataFrame): Training dependent variable
       y_valid (pandas.DataFrame): Validation dependent variable
       max_cardinality (int): Maximum cardinality to apply OneHotEncoder
       regression_model (Any): Regression model
       extra_pipeline_process (Tuple[str, Any]): Additional pipeline processes before build the model
       print_color (str): Color used to print in console

    Attributes:
        _pipeline (Pipeline): Child model regression pipeline
        _X_train (pandas.DataFrame): Selected training independent variables
        _X_valid (pandas.DataFrame): Selected validation independent variables
        _y_train (pandas.DataFrame): Training dependent variable
        _y_valid (pandas.DataFrame): Validation dependent variable
        _interested_cols (List[str]): Columns names to use
        _is_build (bool): Flag that indicates if the model was built
        _max_cardinality (int): Maximum cardinality to apply OneHotEncoder
        _print_color (str): Color used to print in console
        _print_comparison (bool): Flag to compare and print the first 5 elements (True values vs predictions) from the validation data
    """

    def __init__(self, x_train: DataFrame, x_valid: DataFrame, y_train: DataFrame,
                 y_valid: DataFrame, max_cardinality: int,
                 regression_model: Any, extra_pipeline_process: Tuple[str, Any] = None, 
                 print_color:str = 'white', print_comparison: bool = False):
        preprocessor, num_cols, cat_cols_one_hot_encoder, cat_cols_label_encoder = \
            Preprocessing.get_preprocessor_transformer(
                x_train, max_cardinality)

        pipeline_steps = [('preprocessor', preprocessor),
                          ('model', regression_model)]
        if extra_pipeline_process:
            pipeline_steps.insert(1, extra_pipeline_process)
        
        self._print_comparison = print_comparison
        self._print_color = print_color
        self._max_cardinality = max_cardinality
        self._is_build = False
        self._pipeline = Pipeline(steps=pipeline_steps)
        self._interested_cols = num_cols + cat_cols_one_hot_encoder + cat_cols_label_encoder
        # cprint(f'num_cols: {num_cols}', 'blue')
        # cprint(f'cat_cols_one_hot_encoder: {cat_cols_one_hot_encoder}', 'yellow')
        # cprint(f'cat_cols_label_encoder: {cat_cols_label_encoder}', 'green')

        self._X_train = x_train[self._interested_cols].copy()
        self._X_valid = x_valid[self._interested_cols].copy()
        self._y_train = y_train.copy()
        self._y_valid = y_valid.copy()

    def show_sort_comparison_train_vs_valid(self, y_predict: List[float], idx_start: int = 0, idx_end: int = 5) -> None:
        """
        Prints the true values and the predicted values

        Args:
            y_predict (List[float]): Predictions from the validation data
            idx_start (int): List index to start printing
            idx_end (int): List index to end printing

        Returns:
            None
        """
        true_val = list(map(lambda val: f'{val:.2f}', self._y_valid.iloc[idx_start:idx_end].values))
        prediction = list(map(lambda val: f'{val:.2f}', y_predict[idx_start:idx_end]))
        cprint(f'True value: {true_val}', self._print_color)
        cprint(f'Prediction: {prediction}', self._print_color)

    def build_and_evaluate(self) -> float:
        """
        Builds and evaluates the model

        Args:
            print_comparison (bool): Flag to prints the real values and the predicted ones

        Returns:
            float: R2 score obtained with the validation data
        """
        self._pipeline.fit(self._X_train, self._y_train)
        self._is_build = True
        y_predict = self._pipeline.predict(self._X_valid)

        if self._print_comparison:
            self.show_sort_comparison_train_vs_valid(y_predict)
        score_valid = r2_score(self._y_valid, y_predict)

        return score_valid

    def predict(self, x_test: DataFrame) -> List[float]:
        """
        Gets the predictions for testing data

        Args:
            x_test (pandas.DataFrame): Testing independent variables

        Returns:
            List[float]: Testing predictions
        """
        x = x_test[self._interested_cols].copy()
        if not self._is_build:
            warnings.warn(
                "Warning: The model is not yet trained, calling `build` function first.")
            self.build_and_evaluate()
        y_test = self._pipeline.predict(x)
        return y_test

    def get_cross_validation_mean_score(self, num_folds: int, scoring: str) -> Tuple[float, float]:
        """
        Gets the mean and std score for the training performance on cross validation

        Args:
            num_folds (int): Number of folds to use on cross validation
            scoring (str): Metric name to calculate the score

        Returns:
            float: Mean score obtained on the cross validation
            float: Standard deviation score obtained on the cross validation
        """
        scores = cross_val_score(
            self._pipeline, self._X_train, self._y_train, cv=num_folds, scoring=scoring)
        return scores.mean(), scores.std()


class MultipleLinearRegression(AbstractRegression):
    """
    Class to build, evaluate and make predictions using `LinearRegression` class

    Args:
       x_train (pandas.DataFrame): Training independent variables
       x_valid (pandas.DataFrame): Validation independent variables
       y_train (pandas.DataFrame): Training dependent variable
       y_valid (pandas.DataFrame): Validation dependent variable
       max_cardinality (int): Maximum cardinality to apply OneHotEncoder
       print_color (str): Color used to print in console
       print_comparison (bool): Flag to compare and print the first 5 elements (True values vs predictions) from the validation data

    Attributes:
        (inherited attributes from `AbstractRegression` class)
    """

    def __init__(self, x_train: DataFrame, x_valid: DataFrame, y_train: DataFrame,
                 y_valid: DataFrame, max_cardinality: int, 
                 print_color: str, print_comparison: bool):
        model = LinearRegression(
            fit_intercept=True, normalize=False, copy_X=True, n_jobs=None)
        super().__init__(x_train, x_valid, y_train, y_valid, max_cardinality, model, 
                        print_color = print_color, print_comparison = print_comparison)


class PolynomialRegression(AbstractRegression):
    """
    Class to build, evaluate and make predictions using `PolynomialRegression`

    Args:
       x_train (pandas.DataFrame): Training independent variables
       x_valid (pandas.DataFrame): Validation independent variables
       y_train (pandas.DataFrame): Training dependent variable
       y_valid (pandas.DataFrame): Validation dependent variable
       max_cardinality (int): Maximum cardinality to apply OneHotEncoder
       degree (int): Polynomial degree to transform the data
       print_color (str): Color used to print in console
       print_comparison (bool): Flag to compare and print the first 5 elements (True values vs predictions) from the validation data

    Attributes:
        (inherited attributes from `AbstractRegression` class)
        _degree (int): Polynomial degree to transform the data
    """

    def __init__(self, x_train: DataFrame, x_valid: DataFrame, y_train: DataFrame,
                 y_valid: DataFrame, max_cardinality: int, degree: int, 
                 print_color: str, print_comparison: bool):
        self._degree = degree
        poly_transformer_step = ('poly_transformer', PolynomialFeatures(degree=self._degree))
        model = LinearRegression(
            fit_intercept=True, normalize=False, copy_X=True, n_jobs=None)
        super().__init__(x_train, x_valid, y_train, y_valid,
                         max_cardinality, model, poly_transformer_step,
                         print_color = print_color, print_comparison = print_comparison)


class SupportVectorRegression(AbstractRegression):
    """
    Class to build, evaluate and make predictions using `SVR` class

    Args:
       x_train (pandas.DataFrame): Training independent variables
       x_valid (pandas.DataFrame): Validation independent variables
       y_train (pandas.DataFrame): Training dependent variable
       y_valid (pandas.DataFrame): Validation dependent variable
       max_cardinality (int): Maximum cardinality to apply OneHotEncoder
       kernel (str): Support vector regression vector
       print_color (str): Color used to print in console
       print_comparison (bool): Flag to compare and print the first 5 elements (True values vs predictions) from the validation data

    Attributes:
        (inherited attributes from `AbstractRegression` class)
        _kernel (str): Support vector regression vector
    """

    def __init__(self, x_train: DataFrame, x_valid: DataFrame, y_train: DataFrame,
                 y_valid: DataFrame, max_cardinality: int, kernel: str, 
                 print_color: str, print_comparison: bool):
        self._kernel = kernel
        scale_transformer_step = ('scale_transformer', StandardScaler())
        model = SVR(kernel=self._kernel, degree=3, epsilon=0.1, gamma='scale')
        super().__init__(x_train, x_valid, y_train, y_valid,
                         max_cardinality, model, scale_transformer_step,
                         print_color = print_color, print_comparison = print_comparison)


class DecisionTreeRegression(AbstractRegression):
    """
    Class to build, evaluate and make predictions using `DecisionTreeRegressor` class

    Args:
       x_train (pandas.DataFrame): Training independent variables
       x_valid (pandas.DataFrame): Validation independent variables
       y_train (pandas.DataFrame): Training dependent variable
       y_valid (pandas.DataFrame): Validation dependent variable
       max_cardinality (int): Maximum cardinality to apply OneHotEncoder
       random_state (int): Number used for initializing the internal random number generator
       print_color (str): Color used to print in console
       print_comparison (bool): Flag to compare and print the first 5 elements (True values vs predictions) from the validation data

    Attributes:
        (inherited attributes from `AbstractRegression` class)
        _random_state (int): Number used for initializing the internal random number generator
    """

    def __init__(self, x_train: DataFrame, x_valid: DataFrame, y_train: DataFrame,
                 y_valid: DataFrame, max_cardinality: int, random_state: int, 
                 print_color: str, print_comparison: bool):
        self._random_state = random_state
        model = DecisionTreeRegressor(random_state=self._random_state, criterion='mse', splitter='best', max_depth=None,
                                      min_samples_split=2, min_samples_leaf=1)
        super().__init__(x_train, x_valid, y_train, y_valid, max_cardinality, model, 
                        print_color = print_color, print_comparison = print_comparison)


class RandomForestRegression(AbstractRegression):
    """
    Class to build, evaluate and make predictions using `RandomForestRegressor` class

    Args:
       x_train (pandas.DataFrame): Training independent variables
       x_valid (pandas.DataFrame): Validation independent variables
       y_train (pandas.DataFrame): Training dependent variable
       y_valid (pandas.DataFrame): Validation dependent variable
       max_cardinality (int): Maximum cardinality to apply OneHotEncoder
       random_state (int): Number used for initializing the internal random number generator
       num_estimators (int): Number of estimators for Random Forest Regression
       print_color (str): Color used to print in console
       print_comparison (bool): Flag to compare and print the first 5 elements (True values vs predictions) from the validation data

    Attributes:
        (inherited attributes from `AbstractRegression` class)
        _random_state (int): Number used for initializing the internal random number generator
        _num_estimators (int): Number of estimators for Random Forest Regression
    """

    def __init__(self, x_train: DataFrame, x_valid: DataFrame, y_train: DataFrame,
                 y_valid: DataFrame, max_cardinality: int, random_state: int, num_estimators: int,
                 print_color: str, print_comparison: bool):
        self._random_state = random_state
        self._num_estimators = num_estimators
        model = RandomForestRegressor(n_estimators=self._num_estimators, random_state=self._random_state, criterion='mse',
                                      max_depth=None)
        super().__init__(x_train, x_valid, y_train, y_valid, max_cardinality, model, 
                        print_color = print_color, print_comparison = print_comparison)
