
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



def _is_numeric(x):
    """
        Check if the input can be converted to a float.

        Args:
            x: The input to check.

        Returns:
            bool: True if the input can be converted to a float, False otherwise.
    """
    try:
        float(x)
        return True
    except Exception:
        return False

def _is_none_nan_null(x):
    """
        Check if the input value is None, NaN, or Null.

        Parameters:
        x : any type
            The input value to check.

        Returns:
        bool
            True if the input value is None, NaN, or Null, otherwise False.
    """
    return x is None or pd.isnull(x)

def _is_date(x, format:str = "ymd"):
    """
        Check if a given string is a valid date in the specified format.

        Args:
            x (str): The string to check.
            format (str): The date format to validate against.
                        Supported formats are "Ymd" (default), "mdY", and "dmy".

        Returns:
            bool: True if the string is a valid date in the specified format, False otherwise.

        Raises:
            Exception: If an error occurs during date validation.
    """
    is_date = False
    try:
        value = str(x)
        date_split = re.split(r"[/\-]", value)
        if len(date_split) != 3:
            return False
        if format == "ymd":
            regex = re.compile(r"^\d{4}[/\-]\d{2}[/\-]\d{2}$")
            year = len(date_split[0]) == 4
            month = 1<=int(date_split[1])<=12
            day = 1<=int(date_split[2])<=31
            is_date = regex.match(x) and year and month and day
        elif format == "dmy":
            regex = re.compile(r"^\d{2}[/\-]\d{2}[/\-]\d{4}$")
            year = len(date_split[2]) == 4
            month = 1<=int(date_split[1])<=12
            day = 1<=int(date_split[0])<=31
            is_date = regex.match(x) and year and month and day
        elif format == "mdy":
            regex = re.compile(r"^\d{2}[/\-]\d{2}[/\-]\d{4}$")
            year = len(date_split[2]) == 4
            month = 1<=int(date_split[0])<=12
            day = 1<=int(date_split[1])<=31
            is_date = regex.match(x) and year and month and day
        else:
            return False
        return is_date
    except Exception:
        return False

def _is_bool(x):
    """
        Check if the given string represents a boolean value.

        Args:
            x (str): The string to check.

        Returns:
            bool: True if the string is "true" or "false" (case insensitive), False otherwise.
    """
    return x.lower() in ["true", "false"]

def _is_categorical(x):
    """
        Determine if the input value is categorical.

        A value is considered categorical if it is not numeric, not a date,
        not a boolean, and not None, NaN, or null.

        Args:
            x: The input value to be checked.

        Returns:
            bool: True if the input value is categorical, False otherwise.
    """
    return not _is_numeric(x) and not _is_date(x) and not _is_bool(x) and not _is_none_nan_null(x)

def _is_mail(x):
    """
        Check if the given string is a valid email address.

        Args:
            x (str): The string to be checked.

        Returns:
            re.Match or None: A match object if the string is a valid email address, None otherwise.
    """
    regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return regex.match(x)

def _is_url(x):
    """
        Check if the given string is a valid URL.

        Args:
            x (str): The string to be checked.

        Returns:
            re.Match or None: A match object if the string is a valid URL, None otherwise.
    """
    regex = re.compile(r"^(http|https)://[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return regex.match(x)

def _is_phone(x):
    """
        Check if the given string is a valid phone number.

        A valid phone number can optionally start with a '+' followed by 1 to 3 digits,
        and may contain spaces, dashes, or dots as separators. It should have a format
        similar to the following examples:
        - +123 456 789 0123
        - 123-456-7890
        - (123) 456-7890

        Args:
            x (str): The string to be checked.

        Returns:
            re.Match or None: A match object if the string is a valid phone number, None otherwise.
    """
    regex = re.compile(r"^\+?[0-9]{1,3}?[-. ]?\(?[0-9]{3}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}$")
    return regex.match(x)


def infer_type(x):
    """
        Infers the type of the given input `x`.

        The function checks the input against various conditions to determine its type.
        The possible return values are:
        - "nan": if the input is None, NaN, or null.
        - "date_Ymd": if the input is a date in the format "Ymd".
        - "date_mdY": if the input is a date in the format "mdY".
        - "date_dmy": if the input is a date in the format "dmy".
        - "bool": if the input is a boolean.
        - "mail": if the input is an email address.
        - "url": if the input is a URL.
        - "phone": if the input is a phone number.
        - "numeric": if the input is numeric.
        - "categorical": if the input is categorical.
        - "unknown": if the input does not match any of the above conditions.

        Args:
            x: The input value to be checked.

        Returns:
            str: The inferred type of the input.
    """
    if execute_script_v2(_is_none_nan_null, x=x):
        return "nan"
    elif _is_date(x, "ymd") :
        return "date_ymd"
    elif _is_date(x, "dmy") :
        return "date_dmy"
    elif _is_date(x, "mdy") :
        return "date_mdy"
    elif execute_script_v2(_is_bool, x=x):
        return "bool"
    elif execute_script_v2(_is_mail, x=x):
        return "mail"
    elif execute_script_v2(_is_url, x=x):
        return "url"
    elif execute_script_v2(_is_phone, x=x):
        return "phone"
    elif _is_numeric(x):
        return "numeric"
    elif execute_script_v2(_is_categorical, x=x):
        return "categorical"
    else:
        return "unknown"
