import pandas as pd
import os
from loguru import logger

        
def read_file_to_dataframe(input_file, file_info:dict={}):
    """
        Read a file and convert it into a pandas DataFrame or a dictionary of DataFrames if the file contains multiple sheets (e.g., Excel files).

        Parameters:
            input_file (str): The path to the file to be read.
            file_info (dict): A dictionary containing encoding and delimiter information for specific files.

        Returns:
            DataFrame or dict: A DataFrame if the file is a CSV, TXT, or Parquet file. A dictionary of DataFrames if the file is an Excel file with multiple sheets. Returns None if the file type is unsupported.

        Example:
            file_info = {
                "example.csv": {"encodage": "utf-8", "delimiteur": ","}
            }
        df = read_file_to_dataframe("example.csv", file_info)
    """
    logger.info("START the read_file_to_dataframe function")
    
    file_extension = input_file.split('.')[-1].lower()
    file_name = os.path.basename(input_file)
    
    if file_extension in ['csv', 'txt']:
        if file_name in file_info:
            encodage = file_info[file_name]['encodage']
            delimiteur = file_info[file_name]['delimiteur']
            return pd.read_csv(input_file, encoding=encodage, delimiter=delimiteur)
        else:
            print(f"Aucune information spécifique trouvée pour '{file_name}'. Utilisation des paramètres par défaut.")
            return pd.read_csv(input_file)
    elif file_extension == 'xlsx':
        xls = pd.ExcelFile(input_file)
        return {sheet_name: pd.read_excel(xls, sheet_name=sheet_name) for sheet_name in xls.sheet_names}
    elif file_extension == 'parquet':
        return pd.read_parquet(input_file)
    else:
        print(f"Attention : Le fichier '{input_file}' a un type non supporté et a été ignoré.")
        return None

class Reader:
    
    @staticmethod
    def read_all_files_in_directory(directory_path, file_info:dict={}):
        """
            Read all files in the specified directory and convert them into DataFrames.

            Parameters:
                directory_path (str): The path to the directory containing the files to be read.
                file_info (dict, optional): A dictionary containing encoding and delimiter information for specific files.

            Returns:
                dict: A dictionary where the keys are the file names (without extensions) and the values are the corresponding DataFrames. If a file is an Excel file with multiple sheets, the key will be in the format "filename_sheetname".

            Example:
                file_info = {
                    "example.csv": {"encodage": "utf-8", "delimiteur": ","}
                }
            dataframes = Reader.read_all_files_in_directory("/path/to/directory", file_info)
        """
        logger.info("START the Reader.read_all_files_in_directory function")
        
        dataframes = {}
        for filename in os.listdir(directory_path):
            logger.info("Reading file " + filename)
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                df = read_file_to_dataframe(file_path, file_info)
                if df is not None:
                    if isinstance(df, dict):
                        for sheet_name, sheet_df in df.items():
                            key = f"{os.path.splitext(filename)[0]}_{sheet_name}"
                            dataframes[key] = sheet_df
                    else:
                        dataframes[os.path.splitext(filename)[0]] = df
        return dataframes
