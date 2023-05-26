from ecp.logger import logging
import sys
from ecp.exception import CustomException
from ecp.entity import config_entity,artifact_entity
from ecp.predictor import ModelResolver
from ecp.utils import load_object,save_object

class ModelPusher:
    def __init__(self,
                 model_pusher_config :config_entity.ModelPusherConfig,
                 model_trainer_artifact:artifact_entity.ModelTrainerArtifact,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact):
            try:
                self.model_pusher_config = model_pusher_config
                self.model_trainer_artifact = model_trainer_artifact
                self.data_transformation_artifact = data_transformation_artifact
                self.model_resolver = ModelResolver(model_registery=self.model_pusher_config.saved_model_dir)
            except Exception as e:
                 raise CustomException(e, sys)
                    

    def initiate_model_pusher(self):
        try:
            transformer = load_object(filepath=self.data_transformation_artifact.transform_object_path)
            model = load_object(filepath=self.model_trainer_artifact.model_path)
            target_encoder = load_object(filepath=self.data_transformation_artifact.target_encoder_path)

            #model pusher dir
            save_object(filepath=self.model_pusher_config.pusher_transformer_path,obj= transformer)
            save_object(filepath=self.model_pusher_config.model_pusher_dir,obj=model)
            save_object(filepath=self.model_pusher_config.pusher_target_encoder_path,obj=target_encoder)

            #save model

            transformer_path =  self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            save_object(filepath=transformer_path,obj=transformer)
            save_object(filepath=model_path,obj=model)
            save_object(filepath=target_encoder_path,obj= target_encoder)


            model_pusher_artifact = artifact_entity.ModelPusherArtifact(pusher_model_dir=self.model_pusher_config.pusher_model_dir,
                                                                        saved_model_dir=self.model_pusher_config.saved_model_dir)
            
            return model_pusher_artifact
        except Exception as e:
             raise CustomException(e, sys)