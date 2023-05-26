from ecp.exception import CustomException
from ecp.logger import logging
from ecp.entity import config_entity, artifact_entity
import sys,os
import pandas as pd
from ecp import utils
import numpy as np
from sklearn.model_selection import train_test_split


class DataInjestion:
    def __init__(self,data_injestion_config :config_entity.DataInjestionConfig):
        try:
            self.data_injestion_config = data_injestion_config
        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_data_injestion(self)->artifact_entity.DataInjestionArtifact:
        try:
            logging.info(f' Export collection data as pandas dataframe')
            df:pd.DataFrame = utils.get_collection_as_dataframe(
                database_name=self.data_injestion_config.database_name,
                collection_name=self.data_injestion_config.collection_name)
            logging.info('save data in feature store')

            df.replace(to_replace='na',value=np.NaN,inplace=True)

            feature_store_dir = os.path.dirname(self.data_injestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)

            logging.info('save df to feature store')
            df.to_csv(path_or_buf=self.data_injestion_config.feature_store_file_path, index=True, header=True)

            logging.info('spliting df into train and test')
            train_df, test_df = train_test_split(df, test_size=self.data_injestion_config.test_size)

            logging.info('create dataset dir folder if not excist')
            dataset_dir =  os.path.dirname(self.data_injestion_config.test_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info("save dataset to feature store")
            train_df.to_csv(path_or_buf =self.data_injestion_config.train_file_path)
            test_df.to_csv(path_or_buf =self.data_injestion_config.test_file_path)

            data_injestion_artifact = artifact_entity.DataInjestionArtifact(
                feature_store_file_path= self.data_injestion_config.feature_store_file_path,
                train_file_path=self.data_injestion_config.train_file_path,
                test_file_path=self.data_injestion_config.test_file_path
            )

            return data_injestion_artifact

        except Exception as e:
            raise CustomException(e, sys)