from ecp.exception import CustomException
from ecp.logger import logging
from ecp.entity import config_entity 
from ecp.entity import artifact_entity 
import pandas as pd
import os, sys
from typing import Optional
import numpy as np
from ecp.config import TARGET_COLUMN
from ecp import utils
from scipy.stats import ks_2samp
from ecp.entity.artifact_entity import DataValidationArtifact


class DataValidation:
    def __init__(self,
                 data_validation_config:config_entity.DataValidationConfig,
                 data_injestion_config:config_entity.DataInjestionConfig,
                 data_injestion_artifact:artifact_entity.DataInjestionArtifact):
        try:
            logging.info('Data Validation')
            self.data_validation_config = data_validation_config
            self.data_injestion_config = data_injestion_config
            self.data_injestion_artifact = data_injestion_artifact
            self.validaiton_error = dict()


        except Exception as e:
            raise CustomException(e, sys)
        

    def drop_missing_values_columns(self,df:pd.DataFrame,report_key_name:str)->Optional[pd.DataFrame]:
        try:
            logging.info("dropping missing value columns")
            threshold = self.data_validation_config.missing_threshold
            null_report = df.isna().sum()/df.shape[0]
            drop_columns_names = null_report[null_report>threshold].index
            self.validaiton_error[report_key_name] = list(drop_columns_names)

            df.drop(list(drop_columns_names),axis=1,inplace=True)
            if len(df.columns) == 0:
                return 0
            return df

        except Exception as e:
            raise CustomException(e, sys)


    def is_required_columns_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            logging.info('checking for missing columns')
            base_columns = base_df
            current_columns = current_df
            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f'{base_column} is missing')
                    missing_columns.append(base_column)
                
                if len(missing_columns)>0:
                    self.validaiton_error[report_key_name] = missing_columns
                    return False
                return True
            
        except Exception as e:
            raise CustomException(e, sys)        

    def data_drift(self, base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns= current_df.columns

            for base_column in base_columns:
                base_data, current_data = base_df[base_column],current_df[base_column]

                same_distribution = ks_2samp(base_data,current_data)

                if same_distribution.pvalue > 0.05:
                    drift_report[base_column] = {
                        "pvalues" : float(same_distribution.pvalue),
                        "same_distribution":True
                    }
                else:
                    drift_report[base_column] = {
                        "pvalues" : float(same_distribution.pvalue),
                        "same_distribution":False
                    }
            self.validaiton_error[report_key_name] = drift_report
            
        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            logging.info('Initiate Data Validation')
            base_df = pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replace({"na":np.NaN},inplace=True)
            base_df = self.drop_missing_values_columns(df=base_df,report_key_name="Missing_value_within_base_file")


            logging.info("Loading train and test dataset")
            train_df = pd.read_csv(self.data_injestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_injestion_artifact.test_file_path)
            logging.info("train and test df loaded")

            logging.info("checking missing value in train and test")
            train_df = self.drop_missing_values_columns(df=train_df,report_key_name="Missing_value_within_train_file")
            test_df = self.drop_missing_values_columns(df=test_df,report_key_name="Missing_value_within_test_file")
            
            exclude_columns = [TARGET_COLUMN]
            base_df = utils.convert_columns_float(df=base_df,exclude_columns=exclude_columns)
            train_df = utils.convert_columns_float(df=train_df,exclude_columns=exclude_columns)
            test_df = utils.convert_columns_float(df=test_df,exclude_columns=exclude_columns)

            # logging.info(" {train_df.head(2)} ")

            logging.info("is required column exist in train and test df")
            train_df_column_status = self.is_required_columns_exists(base_df=base_df, current_df=train_df,report_key_name="Missing_column_in_train_dataset")
            test_df_column_status = self.is_required_columns_exists(base_df=base_df, current_df=test_df,report_key_name="Missing_column_in_test_dataset")

            if train_df_column_status:
                logging.info("As all the column exist in train df detecting data drift")
                self.data_drift(base_df=base_df,current_df=train_df,report_key_name="Data_drift_within_train_dataset")
                
            if test_df_column_status:
                logging.info("As all the column exist in test df detecting data drift")
                self.data_drift(base_df=base_df,current_df=test_df,report_key_name="Data_drift_within_train_dataset")

            logging.info("Write report in yaml file")
            utils.write_yaml_file(filepath=self.data_validation_config.report_file_path,
                                  data=self.validaiton_error)
            

            data_validation_artifact =DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)


            return data_validation_artifact


        except Exception as e:
            raise CustomException(e, sys)