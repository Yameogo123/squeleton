
#%% import
from {{ cookiecutter.package_slug }}.utils.reader import Reader
from loguru import logger
from {{ cookiecutter.package_slug }}.data.analysis.analysis import save_desc, get_correlation, detect_errors
from {{ cookiecutter.package_slug }}.utils.utils import save_to_parquet
from skimpy import skim
import os
from tabulate import tabulate
import pretty_errors

#%% variables

PROCESSED_PATH = "../data/processed"
OUTPUT_PATH = "../reports/analysis"

os.makedirs(OUTPUT_PATH+"/description", exist_ok=True)
os.makedirs(OUTPUT_PATH+"/correlation", exist_ok=True)
os.makedirs(OUTPUT_PATH+"/detection", exist_ok=True)

save_description = True
save_correlation = True

logger.info(f"Load data from {PROCESSED_PATH}")
dataframes = Reader.read_all_files_in_directory(PROCESSED_PATH)


#%% data preview


for name in dataframes.keys():
    df = dataframes[name]
    logger.info("===============================================")

    logger.info(f"==== SAVE DESCRIPTION OF {name} ====")
    skim(df)
    if save_description:
        logger.info(f"saving description in {OUTPUT_PATH}/description")
        save_desc(df, f"{OUTPUT_PATH}/description", name)
    logger.info("-----------------------------------------------")
    logger.info(f"==== Disquality OF {name} DATA ====")
    errors = detect_errors(df)
    if not errors.empty:
        logger.info(f"saving disqualities in {OUTPUT_PATH}/detection")
        save_to_parquet(errors, f"{OUTPUT_PATH}/detection/{name}.parquet")

    logger.info(f"==== SAVE CORRELATION OF {name} DATA ====")
    corrs = get_correlation(df)
    if save_correlation:
        logger.info(f"saving errors in {OUTPUT_PATH}/correlation")
        save_to_parquet(corrs, f"{OUTPUT_PATH}/correlation/{name}.parquet")
    print(tabulate(corrs, headers='keys', tablefmt='grid'))
    logger.info("-----------------------------------------------")


# %%

