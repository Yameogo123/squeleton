
import pandas as pd
from loguru import logger
from flaml.automl.automl import AutoML
from {{ cookiecutter.package_slug }}.utils.utils import are_df_columns


def supervised_automl(df: pd.DataFrame, task: str, target: str):
    """
        Perform automated machine learning (AutoML) for a supervised learning task.

        Parameters:
            df (pd.DataFrame): The input dataframe containing the features and target column.
            task (str): The type of supervised learning task ('classification' or 'regression').
            target (str): The name of the target column in the dataframe.

        Returns:
            AutoML: The trained AutoML model with the best configuration found.

        Raises:
            ValueError: If the target column is not found in the dataframe.

        Example:
            >>> model = supervised_automl(df, task='classification', target='label')
            >>> print(model.model.__class__.__name__)
            >>> print(model.best_config)
    """
    if not are_df_columns(df, [target]):
        raise ValueError(f"Target column {target} not found in the dataframe")
    model = AutoML()
    logger.info(f"Running AutoML for {task} task")
    X = df.drop(columns=[target])
    y = df[target]
    model.fit(X, y, task=task)
    logger.info(f"Best model found: {model.model.__class__.__name__}")
    logger.info(f"Best model parameters: {model.best_config}")
    return model
