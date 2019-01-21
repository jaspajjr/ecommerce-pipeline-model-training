from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn import metrics
import pandas as pd


def calculate_metrics(y_true, y_pred) -> dict:
    return {
        'mean_squared_error': metrics.mean_squared_error(y_true, y_pred),
        'mean_abs_error': metrics.mean_absolute_error(y_true, y_pred),
        'median_abs_error': metrics.median_absolute_error(y_true, y_pred),
        'r2_score': metrics.r2_score(y_true, y_pred)
    }


def fit_linear_regression(X, y) -> LinearRegression:
    model = LinearRegression().fit(X, y)
    return model


def validation(X, y) -> dict:
    validation_list = []

    for train_index, test_index in KFold(n_splits=10).split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        model = fit_linear_regression(X_train, y_train)

        validation_list.append(
            calculate_metrics(y_test, model.predict(X_test)))

    return pd.DataFrame(validation_list)
