from ECP.logger import logging
from ECP.exception import CustomException
import sys,pandas as pd
from ECP.config import mongo_client


def get_collection_as_dataframe(database_name:str,collection_name:str):
    try:
        logging.info(f"Reading data from database :{database_name} and collection: {collection_name}")
        df = pd.DataFrame(mongo_client[database_name][collection_name].find())
        logging.info(f"Dataframe shape is {df.shape}")
        if "_id" in df.columns:
            logging.info("droping _id column")
            df.drop(columns="_id",inplace=True)
        logging.info(f"rows and columns in df {df.shape}")
        return df

    except Exception as e:
        raise CustomException(e, sys)