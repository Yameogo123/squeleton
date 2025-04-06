import pandas as pd
from loguru import logger
from {{ cookiecutter.package_slug }}.utils.utils import execute_script

from {{ cookiecutter.package_slug }}.models.autoML._timeseries import time_series_automl
from {{ cookiecutter.package_slug }}.models.autoML._unsupervised import unsupervised_automl
from {{ cookiecutter.package_slug }}.models.autoML._supervised import supervised_automl



def automl(df: pd.DataFrame, task: str = "classification", target: str = "", n_clusters: int = 4):
    """
        Perform automated machine learning tasks including classification, regression, clustering, and time series analysis.

        Parameters:
            df (pd.DataFrame): The input dataframe containing the dataset.
            task (str): The type of machine learning task to perform. Supported tasks are "classification", "regression", "clustering", and "time_series". Default is "classification".
            target (str): The target column name for supervised tasks (classification, regression) or the date column for time series tasks. Default is an empty string.
            n_clusters (int): The number of clusters to form for clustering tasks. Default is 4.

        Returns:
            The result of the executed automated machine learning task.

        Raises:
            ValueError: If the specified task is not supported.
    """
    logger.info("Can take a while depending on the dataset size")
    if task == "classification" or task == "regression":
        return execute_script(supervised_automl, df=df, task=task, target=target)
    elif task == "clustering":
        return execute_script(unsupervised_automl, df=df, n_clusters=n_clusters)
    elif task == "time_series":
        return execute_script(time_series_automl, df= df, date=target)
    else:
        raise ValueError(f"Task {task} not supported. Supported tasks are classification, regression, time_series and clustering")

