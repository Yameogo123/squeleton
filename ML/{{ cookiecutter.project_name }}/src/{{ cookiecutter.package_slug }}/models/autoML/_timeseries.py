import pandas as pd
from loguru import logger
from {{ cookiecutter.package_slug }}.utils.utils import are_df_columns

from autots import AutoTS

def time_series_automl(df: pd.DataFrame, date: str):
    """
        Perform automated time series forecasting using multiple models and return the best model.

        Parameters:
            df (pd.DataFrame): The input dataframe containing the time series data.
            date (str): The name of the column in the dataframe that contains the date information.

        Returns:
            model: The best model found during the automated time series forecasting process.

        Raises:
            ValueError: If the target column specified by `date` is not found in the dataframe.

        Example:
            >>> import pandas as pd
            >>> from some_module import time_series_automl
            >>> df = pd.DataFrame({
            ...     'date': ['2021-01-01', '2021-01-02', '2021-01-03'],
            ...     'value': [10, 15, 20]
            ... })
            >>> best_model = time_series_automl(df, 'date')
            >>> print(best_model)
    """
    if not are_df_columns(df, [date]):
        raise ValueError(f"Target column {date} not found in the dataframe")
    df[date] = pd.to_datetime(df[date])
    df0 = df.set_index(date)
    model_list = ['ARIMA', 'ETS', 'Prophet', 'SeasonalNaive']
    logger.info("Running AutoTS")
    model = AutoTS(
        forecast_length=12,  model_list=model_list,
        max_generations=2, num_validations=2, verbose=0           
    )
    model.fit(df0)
    bstname = model.best_model_name
    logger.info(f"Best model found: {bstname}")
    return model.best_model