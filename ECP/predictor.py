from ecp.entity.config_entity import TRANSFORM_OBJECT_PATH_NAME,MODEL_FILE_NAME,TARGET_ENCODER_OBJECT_NAME
from typing import Optional
from ecp.exception import CustomException
import os,sys


class ModelResolver:
    def __init__(self,
                 model_registery:str="artifact",
                 transformer_dir_name="data_transformation\\tranformer",
                 target_encoder_dir_name="data_transformation\\target_encoder",
                 model_dir_name="model_trainer\model"):
        self.model_registery = model_registery
        os.makedirs(self.model_registery,exist_ok=True)
        self.transformer_dir_name = transformer_dir_name
        self.target_encoder_dir_name = target_encoder_dir_name
        self.model_dir_name = model_dir_name

    def get_latest_dir_path(self)->Optional[str]:
        try:
            dir_name = os.listdir(self.model_registery)
            if len(dir_name)==0:
                return None
            dir_name = list(map(int,dir_name))
            latest_dir_name = max(dir_name)
            return os.path.join(self.model_registery,f"{latest_dir_name}")
        
        except Exception as e:
            raise CustomException(e, sys)


    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception("Model is not available")
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        except Exception as e:
            raise CustomException(e, sys)
        
    
    def get_latest_transformer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception("Transformer is not available")
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORM_OBJECT_PATH_NAME)
        except Exception as e:
            raise CustomException(e, sys)
        
    
    
    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception("Target Encoder is not available")
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_NAME)
        except Exception as e:
            raise CustomException(e, sys)
        
    
    def get_latest_save_dir_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                return os.path.join(self.model_registery,f"{0}")
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))
            return os.path.join(self.model_registery,f"{latest_dir_num + 1}")
        
        except Exception as e:
            raise CustomException(e, sys)
        
    
    def get_latest_save_model_path(self):
        try:
            latest_dir = self.get_latest_save_model_path()
            return os.path.join(latest_dir,self.model_dir_name,MODEL_FILE_NAME)
        
        except Exception as e:
            raise CustomException(e, sys)    
        
    
    def get_latest_save_transformer_path(self):
        try:
            latest_dir = self.get_latest_save_model_path()
            return os.path.join(latest_dir,self.transformer_dir_name,TRANSFORM_OBJECT_PATH_NAME)
        
        except Exception as e:
            raise CustomException(e, sys)
        

    
    def get_latest_save_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_save_model_path()
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT_NAME)
        
        except Exception as e:
            raise CustomException(e, sys)