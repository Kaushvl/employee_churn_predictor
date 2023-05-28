from ecp.exception import CustomException
from ecp.logger import logging
import sys
from ecp.entity import config_entity
from ecp.components.data_injestion import DataInjestion
from ecp.components.data_validation import DataValidation
from ecp.components.data_transformation import DataTransformation
from ecp.components.model_trainer import ModelTrainer
from ecp.components.model_evaluation import ModelEvaluation
from ecp.components.model_pusher import ModelPusher


def start_trainig_pipeline():
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()

        data_injestion_config = config_entity.DataInjestionConfig(training_pipeline_config=training_pipeline_config)
        print(data_injestion_config.to_dict())

        data_injestion = DataInjestion(data_injestion_config=data_injestion_config)
        data_injestion_artifact = data_injestion.initiate_data_injestion()

        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,
                                         data_injestion_config=data_injestion_config,
                                         data_injestion_artifact=data_injestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()


        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_tarnsformatin = DataTransformation(data_transformation_config=data_transformation_config,data_injestion_artifact=data_injestion_artifact)
        data_transformation_artifact = data_tarnsformatin.initiate_data_transformation()


        model_trainer_config  = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()

   
        model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_eval = ModelEvaluation(model_eval_config=model_eval_config,data_injestion_artifact=data_injestion_artifact,data_transformation_artifact=data_transformation_artifact,model_trainer_artifact=model_trainer_artifact)
        model_eval_artifact = model_eval.initiate_model_evaluation()

        model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config=training_pipeline_config)
        model_pusher = ModelPusher(model_pusher_config=model_pusher_config,model_trainer_artifact=model_trainer_artifact,data_transformation_artifact=data_transformation_artifact)
        model_pusher_artifact = model_pusher.initiate_model_pusher()


    except Exception as e:
        raise CustomException(e, sys)