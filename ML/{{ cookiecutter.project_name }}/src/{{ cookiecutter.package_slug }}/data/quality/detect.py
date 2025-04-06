
from {{ cookiecutter.package_slug }}.utils.utils import infer_type
import pandas as pd
import numpy as np

def handle_type_test(df:pd.DataFrame):
    """
        Analyzes the data types of each column in the given DataFrame and identifies potential type inconsistencies.

        Parameters:
        df (pd.DataFrame): The input DataFrame to be analyzed.

        Returns:
        pd.DataFrame: A DataFrame with additional columns indicating the inferred type of each value and whether it matches the most frequent type in its column.
    """
    df_copy = pd.DataFrame()
    for col in df.columns:
        df_copy[f"{col}_§_type"] = df[col].apply(infer_type)
        try:
            valc = df_copy[f"{col}_§_type"].value_counts().idxmax()
        except Exception:
            valc = "unknown"
        # all that are not the most frequent type are considered as errors
        df_copy[f"{col}_§_supposition"] = df_copy[f"{col}_§_type"].apply(lambda x: "good" if x == valc else "bad")
    return df_copy


def infer_true_type(df:pd.DataFrame):
    """
        Infers the true data type of each column in the given DataFrame and converts the columns to the inferred types.

        This function first checks the data types of the columns using the `handle_type_test` function. It then iterates 
        through each column and replaces values that are identified as "bad" with NaN. Based on the most frequent type 
        detected for each column, it converts the column to the appropriate data type.

        Parameters:
            df (pd.DataFrame): The input DataFrame whose columns' data types need to be inferred and converted.

        Returns:
            None: The function modifies the input DataFrame in place.

        Notes:
            - The function handles the following data types: datetime (in various formats), numeric, object (including mail, 
            url, phone, categorical, unknown), and boolean.
            - If an exception occurs during type inference, the column is converted to the object type by default.
    """
    # get the types of each row of each column
    check = handle_type_test(df)
    dff = df.copy()
    for col in df.columns:
        # get the bad type and put na
        if f"{col}_§_supposition" in check.columns:
            bad = check[f"{col}_§_supposition"] == "bad"
            dff.loc[bad.fillna(False), col] = np.nan

        try:
            if f"{col}_§_type" in check.columns:
                most_frequent = check[f"{col}_§_type"].mode()
                most_frequent = most_frequent[0] if not most_frequent.empty else "object"
            else:
                most_frequent = "object"

            # Définir le bon type
            if most_frequent in ["date_Ymd", "date_mdY", "date_dmY"]:
                dff[col] = pd.to_datetime(dff[col], errors='coerce')
            elif most_frequent == "numeric":
                dff[col] = pd.to_numeric(dff[col], errors='coerce')
            elif most_frequent in ["mail", "url", "phone", "categorical", "unknown"]:
                dff[col] = dff[col].astype("object")
            elif most_frequent == "bool":
                dff[col] = dff[col].astype("bool")
            else:
                dff[col] = dff[col].astype("object")

        except Exception as e:
            print(f"⚠️ Erreur sur la colonne {col}: {e}")
            dff[col] = dff[col].astype("object")  # Sécurité en cas d'erreur

    return dff


def get_errors(df: pd.DataFrame):
    """
        Detects and returns errors in the given DataFrame based on type tests.

        Parameters:
            df (pd.DataFrame): The DataFrame to be checked for errors.

        Returns:
            pd.DataFrame: A DataFrame containing the detected errors with the following columns:
                - id: The index or ID of the row with the error.
                - column: The name of the column with the error.
                - value_in_error: The erroneous value detected.
                - detected_type: The detected type of the erroneous value.
    """
    dico_err = {"id": [], "column": [], "value_in_error": [], "detected_type": []}
    types = handle_type_test(df)

    for col in df.columns:
        cond = types[f"{col}_§_supposition"]=="bad"
        tp = types.loc[cond]

        if tp.empty:
            continue

        n = tp.shape[0]
        idx = idx = tp["_id_"].values if "_id_" in tp.columns else df.index[cond]

        value_in_error = df.loc[cond, col].values[:n]
        detected_type = tp[f"{col}_§_type"].values[:n]

        dico_err["id"] += list(idx)
        dico_err["column"] += [col]*n
        dico_err["value_in_error"] += list(value_in_error)
        dico_err["detected_type"] += list(detected_type)
    errs = pd.DataFrame(dico_err)
    return errs