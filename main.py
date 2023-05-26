from ecp.exception import CustomException
from ecp.logger import logging
import sys
from ecp.entity import config_entity
from ecp.components.data_injestion import DataInjestion
from ecp.components.data_validation import DataValidation
from ecp.components.data_transformation import DataTransformation
from ecp.components.model_trainer import ModelTrainer



# def test_logger_and_exception():
    # try:
    #     logging.info("Starting point the test_logger_and_exception")
    #     result = 3/0
    #     print(result)
    #     logging.info("Ending point the test_logger_and_exception")
    # except Exception as e:
    #     logging.debug(str(e))
    #     raise CustomException(e, sys)
    
if __name__ == '__main__':
    try:
        # test_logger_and_exception()
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

   
    except Exception as e:
        raise CustomException(e, sys)