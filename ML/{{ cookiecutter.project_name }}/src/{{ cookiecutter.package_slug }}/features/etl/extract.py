from dagster import op
from {{ cookiecutter.package_slug }}.utils.reader import Reader
from loguru import logger
import os

RAW_PATH = os.path.join("..", "data", "raw")
INTERM_PATH = os.path.join("..", "data", "interm")

@op
def load_data(context):
    """
        Loads data from a specified raw path, transforms it, and saves it as parquet files.

        Args:
            context: An object that contains logging information.

        Returns:
            dict: A dictionary where keys are dataframe names and values are the corresponding dataframes.

        Logs:
            Logs the loading of data from the raw path and the transformation of each dataframe into parquet format.
    """
    file_path = RAW_PATH
    output_path = INTERM_PATH
    context.log.info(f"Loaded data from {file_path}")
    logger.info(f"Loaded data from {file_path}")
    dataframes = Reader.read_all_files_in_directory(file_path)
    for df_name, df in dataframes.items():
        context.log.info(f"transformed {df_name} into parquet")
        logger.info(f"transformed {df_name} into parquet")
        df.to_parquet(output_path+"/"+df_name+".parquet")
    return dataframes