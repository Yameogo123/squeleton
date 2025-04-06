from loguru import logger
from {{ cookiecutter.package_slug }}.data.quality.detect import infer_true_type, get_errors
import pandas as pd
from skimpy import skim_get_data
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import chi2_contingency
from itertools import combinations

def save_desc(df: pd.DataFrame, output_dir: str, name: str):
    """
        Save descriptive statistics of a DataFrame to CSV files.

        This function generates descriptive statistics for the given DataFrame
        using the `skim_get_data` function and saves the results to CSV files
        in the specified output directory. Each type of descriptive statistic
        is saved in a separate CSV file.

        Parameters:
            df (pd.DataFrame): The DataFrame for which to generate descriptive statistics.
            output_dir (str): The directory where the CSV files will be saved.
            name (str): The base name for the output CSV files.

        Returns:
            None
    """
    description = skim_get_data(df)
    for desc in description.keys():
        if desc not in ['Data Summary', 'Data Types']:
            logger.info(f"saving...: {output_dir}/{name}_{desc}_description.parquet")
            pd.DataFrame(description[desc]).astype(str).to_parquet(f"{output_dir}/{name}_{desc}_description.parquet")



# spearman
def _nums_correlation(df: pd.DataFrame, col1: str, col2: str):
    """
        Calculate the Spearman correlation between two columns in a DataFrame.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the data.
            col1 (str): The name of the first column.
            col2 (str): The name of the second column.

        Returns:
            float: The Spearman correlation coefficient between the two columns.
               Returns NaN if the DataFrame is empty after dropping NaN values
               or if an exception occurs during the calculation.
    """
    try:
        ratio = float(df[col1].corr(df[col2], method="spearman"))
    except Exception as e:
        print(e)
        ratio = np.nan
    return ratio

# v_cramer
def _cats_correlation(df: pd.DataFrame, col1: str, col2: str):
    """
        Calculate the correlation between two categorical variables using the Cramér's V statistic.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the data.
            col1 (str): The name of the first categorical column.
            col2 (str): The name of the second categorical column.

        Returns:
            float: The Cramer's V statistic, which measures the association between two categorical variables.
               Returns np.nan if the DataFrame is empty after dropping NaN values in the specified columns.
    """
    confusion_matrix = pd.crosstab(df[col1], df[col2])
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    return np.sqrt(chi2 / (n * (min(confusion_matrix.shape) - 1)))

# anova
def _mixed_correlation(df: pd.DataFrame, num: str, cat: str):
    """
        Calculate the eta-squared (η²) correlation between a numerical and a categorical variable using ANOVA.

        Parameters:
            df (pd.DataFrame): The input DataFrame containing the data.
            num (str): The name of the numerical column.
            cat (str): The name of the categorical column.

        Returns:
            float: The eta-squared (η²) value representing the proportion of variance in the numerical variable explained by the categorical variable. Returns np.nan if the DataFrame is empty after dropping NaNs.
    """
    # Fit the ANOVA model
    model = ols(f'{num} ~ C({cat})', data=df).fit()
    # Perform ANOVA
    anova_table = sm.stats.anova_lm(model, typ=2)
    #Compute eta-squared (η²) = SS_between / (SS_between + SS_within)
    ss_between = anova_table['sum_sq'].iloc[0]  # Sum of squares for the categorical variable
    ss_total = ss_between + anova_table['sum_sq'].iloc[1]  # Total sum of squares
    eta_squared = ss_between / ss_total if ss_total != 0 else np.nan
    # cr = 1 - anova_table.iloc[0]["PR(>F)"]
    return eta_squared


def _correlation(df:pd.DataFrame, col1:str, col2:str, algorithm:str):
    """
        Calculate the correlation between two columns in a DataFrame using the specified algorithm.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the data.
            col1 (str): The name of the first column.
            col2 (str): The name of the second column.
            algorithm (str): The algorithm to use for calculating the correlation. 
                         Options are "spearman", "anova", and "v_cramer".

        Returns:
            float: The correlation value between the two columns.
    """
    corr = np.nan
    dff = df.dropna(subset=[col1, col2]).copy()
    if dff.empty:
        return np.nan
    if algorithm == "spearman":
       corr = _nums_correlation(dff, col1, col2)
    elif algorithm == "anova":
        try:
            corr = _mixed_correlation(dff, col1, col2)
        except Exception:
            try:
                corr = _mixed_correlation(dff, col2, col1)
            except Exception:
                pass
    elif algorithm == "v_cramer":
        corr = _cats_correlation(dff, col1, col2)
    return corr
    


def get_correlation(df:pd.DataFrame):
    """
        Calculate the correlation between all pairs of columns in a DataFrame.

        Parameters:
            df (pd.DataFrame): The input DataFrame containing the data.

        Returns:
            pd.DataFrame: A DataFrame containing the pairs of columns, their data types, 
                      the algorithm used for correlation, and the correlation values.

            The returned DataFrame has the following columns:
            - 'variable 1': The first variable in the pair.
            - 'variable 2': The second variable in the pair.
            - 'type 1': The data type of the first variable.
            - 'type 2': The data type of the second variable.
            - 'types': A string combining the data types of both variables.
            - 'algorithm': The algorithm used to calculate the correlation ('spearman', 'v_cramer', 'anova', or 'no correlation').
            - 'correlation': The calculated correlation value.
    """
    dff = df.copy()
    if "_id_" in df.columns:
        dff = df.drop(columns=["_id_"])
    cols = dff.columns
    combi = np.array(list(combinations(cols, 2)))
    column_a, column_b = combi[:,0], combi[:,1]
    dico = {"variable 1": column_a, "variable 2": column_b}
    dataframe = pd.DataFrame(dico)
    dff = infer_true_type(dff)
    dataframe["type 1"] = dataframe["variable 1"].map(lambda x: dff[x].dtype)
    dataframe["type 2"] = dataframe["variable 2"].map(lambda x: dff[x].dtype)
    dataframe["types"]  = dataframe["type 1"].astype(str) + "|" + dataframe["type 2"].astype(str)
    dataframe["algorithm"] = np.where(
        dataframe["types"]=="float64|float64", "spearman",
        np.where(
            dataframe["types"] == "object|object", "v_cramer", 
            np.where(
                dataframe["types"].isin(["object|float64", "float64|object"]), "anova", "no correlation"
            )
        )
    )
    dataframe["correlation"] = dataframe.apply(lambda x: _correlation(dff, x["variable 1"], x["variable 2"], x["algorithm"]), axis=1)
    return dataframe
    


def detect_errors(df:pd.DataFrame):
    """
        Detects errors in the given DataFrame.

        This function attempts to detect errors in the provided DataFrame by calling
        the `get_errors` function. If an exception occurs during the process, it 
        returns an empty DataFrame.

        Parameters:
        df (pd.DataFrame): The DataFrame to be analyzed for errors.

        Returns:
        pd.DataFrame: A DataFrame containing the detected errors, or an empty DataFrame
                      if an exception occurs.
     """
    try:
        return get_errors(df)
    except Exception:
        return pd.DataFrame()


