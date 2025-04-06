from dagster import op, AssetMaterialization, MetadataValue, Out
from loguru import logger
import os 

PROCESSSED_PATH = os.path.join("..", "data", "processed")

@op(out=Out(is_required=False))
def save_data(context, dataframes: dict):
    """
        Save processed dataframes to parquet files and log the asset materialization.

        Args:
            context: The context object, typically used for logging.
            dataframes (dict): A dictionary where keys are dataframe names and values are pandas DataFrame objects.

        Yields:
            AssetMaterialization: An event indicating that the asset has been materialized, with metadata about the saved files.
    """
    output_path = PROCESSSED_PATH
    for df_name, df in dataframes.items():
        context.log.info(f"Saved processed data to {df_name}")
        logger.info(f"Saved processed data to {df_name}")
        df.to_parquet(output_path+"/"+df_name+".parquet")
        # Log an asset materialization
        yield AssetMaterialization(
            asset_key="processed_data",
            description="Processed data saved to parquet",
            metadata={
                "output_path": MetadataValue.path(output_path),
                "num_rows": MetadataValue.int(len(df)),
            },
        )
