
import pandas as pd
import re

def are_df_columns(df:pd.DataFrame, columns:list):
    """
        Check if the specified columns are present in the DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to check.
            columns (list): A list of column names to check for in the DataFrame.

        Returns:
            bool: True if all specified columns are present in the DataFrame, False otherwise.
    """
    return set(columns).issubset(df.columns)


def execute_script(function, message:str="erreur de script: ", *args, **kwargs):
    """
        Executes a given function with provided arguments and keyword arguments,
        and handles exceptions by raising a ValueError with a custom message.

        Parameters:
            function (callable): The function to be executed.
            message (str, optional): Custom error message to be prefixed in case of an exception. Defaults to "erreur de script: ".
            *args: Variable length argument list to be passed to the function.
            **kwargs: Arbitrary keyword arguments to be passed to the function.

        Returns:
            Any: The return value of the executed function.

        Raises:
            ValueError: If an exception occurs during the execution of the function, 
                    a ValueError is raised with the provided custom message and the original exception message.
    """
    try:
        return function(*args, **kwargs)
    except Exception as e:
        raise ValueError(f"{message}: {e}")

def execute_script_v2(function, *args, **kwargs):
    """
        Executes a given function with provided arguments and keyword arguments.

        Args:
            function (callable): The function to be executed.
            *args: Variable length argument list to pass to the function.
            **kwargs: Arbitrary keyword arguments to pass to the function.

        Returns:
            The return value of the function if it executes successfully, otherwise returns False.

        Raises:
            Exception: Catches all exceptions and returns False.
    """
    try:
        return function(*args, **kwargs)
    except Exception:
        return False



def save_to_parquet(df:pd.DataFrame, file:str, index:bool = False):
    """
        Save a pandas DataFrame to a Parquet file.

        Parameters:
            df (pd.DataFrame): The DataFrame to save.
            file (str): The file path where the Parquet file will be saved.
            index (bool, optional): Whether to include the DataFrame's index in the output file. Defaults to False.

        Returns:
            None
        """
    df.astype(str).to_parquet(f"{file}", index=index)


def rename_column(df:pd.DataFrame):
    """
        Rename columns of the DataFrame by replacing spaces and punctuations with underscores and converting to lowercase.

        Args:
            df (pd.DataFrame): The DataFrame whose columns need to be renamed.

        Returns:
            pd.DataFrame: The DataFrame with renamed columns.
    """
    df.columns = [re.sub(r'[^\w\s]', '_', col).replace(' ', '_').lower() for col in df.columns]
    return df

