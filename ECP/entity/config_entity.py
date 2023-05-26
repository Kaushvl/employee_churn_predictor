import os,sys
from ecp.exception import CustomException
from datetime import datetime

FILE_NAME = 'employee_data.csv'
TRAIN_FILE_PATH = 'train.csv'
TEST_FILE_PATH = 'test.csv'
TRANSFORM_OBJECT_PATH_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = 'model.pkl'


class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%y%m%d%H%M%S')}")
        except Exception as e:
            raise CustomException(e, sys)

class DataInjestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name = "employee_details"
            self.collection_name = "employee_database"
            self.data_injestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_injestion")
            self.feature_store_file_path = os.path.join(self.data_injestion_dir,'feature_store',FILE_NAME)
            self.train_file_path = os.path.join(self.data_injestion_dir,'dataset',TRAIN_FILE_PATH)
            self.test_file_path = os.path.join(self.data_injestion_dir,'dataset',TEST_FILE_PATH)            
            self.test_size = 0.2

        except Exception as e:
            raise CustomException(e, sys)
        
    def to_dict(self)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise CustomException(e, sys)
        

class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_validation")
            self.report_file_path = os.path.join(self.data_validation_dir, "report.yaml")
            self.missing_threshold:float = 0.2
            self.base_file_path = os.path.join("employee_data.csv")
        except Exception as e:
            raise CustomException(e, sys)
    
class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,'data_transformation')
            self.tranform_object_path = os.path.join(self.data_transformation_dir,"tranformer",TRANSFORM_OBJECT_PATH_NAME)
            self.transform_train_path = os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE_PATH.replace("csv","npz"))
            self.transform_test_path = os.path.join(self.data_transformation_dir,"transformed",TEST_FILE_PATH.replace("csv","npz"))
            self.target_encoder_path = os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_NAME)

        except Exception as e:
            raise CustomException(e, sys)

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir,'model_trainer')
            self.model_path = os.path.join(self.model_trainer_dir,'model',MODEL_FILE_NAME)
            self.expected_accuracy = 0.7
            self.overfitting_threshold = 0.3
            
        except Exception as e:
            raise CustomException(e, sys)
        
class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.change_threshold = 0.01
        except Exception as e:
            raise CustomException(e, sys)
        

# class ModelPusherConfig:
#     def __init__(self,training_pipeline_config:TrainingPipelineConfig):
#         try:
#             self.model_pusher_dir = os.path.join(training_pipeline_config.artifact_dir,"model_pusher_file")
#             self.saved_model_dir = os.path.join("saved_models")
#             self.pusher_model_dir = os.path.join(self.model_pusher_dir,"saved_models")
#             self.pusher_model_path = os.path.join(self.pusher_model_dir,MODEL_FILE_NAME)
#             self.pusher_transformer_path = os.path.join(self.pusher_model_dir,TRANSFORM_OBJECT_PATH_NAME)
#             self.pusher_target_encoder_path = os.path.join(self.pusher_model_dir,TARGET_ENCODER_OBJECT_NAME)
#         except Exception as e :
#             raise CustomException(e, sys)
        

class ModelPusherConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_pusher_dir = os.path.join(training_pipeline_config.artifact_dir , "model_pusher")
        self.saved_model_dir = os.path.join("saved_models")
        self.pusher_model_dir = os.path.join(self.model_pusher_dir,"saved_models")
        self.pusher_model_path = os.path.join(self.pusher_model_dir,MODEL_FILE_NAME)
        self.pusher_transformer_path = os.path.join(self.pusher_model_dir,TRANSFORM_OBJECT_PATH_NAME)
        self.pusher_target_encoder_path = os.path.join(self.pusher_model_dir,TARGET_ENCODER_OBJECT_NAME)