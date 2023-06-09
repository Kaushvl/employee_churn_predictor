from ecp.logger import logging
from ecp.exception import CustomException
from ecp.entity import config_entity, artifact_entity
import sys
from ecp.predictor import ModelResolver
from ecp.utils import load_object
import pandas as pd
from ecp.config import TARGET_COLUMN
from sklearn.metrics import accuracy_score

class ModelEvaluation:
    def __init__(self,
                 model_trainer_artifact:artifact_entity.ModelTrainerArtifact,
                 model_eval_config:config_entity.ModelEvaluationConfig,
                 data_injestion_artifact:artifact_entity.DataInjestionArtifact,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            self.model_trainer_artifact = model_trainer_artifact
            self.model_eval_config = model_eval_config
            self.data_injestion_artifact = data_injestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path == None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(
                    is_model_accepted=True,
                    improved_accuracy=None
                )
                logging.info(f"model eval artifact {model_eval_artifact}")
                return model_eval_artifact
            
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            #for previous model
            transformer = load_object(transformer_path)
            model = load_object(model_path)
            target_encoder = load_object(target_encoder_path)


            #for current model
            current_transformer = load_object(filepath=self.data_transformation_artifact.transform_object_path)
            current_model = load_object(filepath=self.model_trainer_artifact.model_path)
            current_target_encoder = load_object(filepath=self.data_transformation_artifact.target_encoder_path)


            test_df = pd.read_csv(self.data_injestion_artifact.test_file_path)
            target_df = test_df[TARGET_COLUMN]
            y_true = target_df

            input_feature_names = list(transformer.feature_names_in_)

            for i in input_feature_names:
                if test_df[i].dtype == 'object':
                    test_df[i] = target_encoder.fit_transform(test_df[i])

            input_arr = transformer.transform(test_df[input_feature_names])
            y_pred = model.predict(input_arr)

            #previous model accuracy 
            previous_model_acc = accuracy_score(y_true=y_true,y_pred=y_pred)

            #current model accuracy
            input_feature_names = list(current_transformer.feature_names_in_)
            input_arr = current_transformer.transform(test_df[input_feature_names])

            y_pred = current_model.predict(input_arr)
            y_true = target_df

            current_model_acc = accuracy_score(y_true=y_true,y_pred=y_pred)


            if current_model_acc <= previous_model_acc:
                logging.info("current model is not better than previous model")
                raise Exception("current model is not better than previous model")

            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                                                                          improved_accuracy=current_model_acc-previous_model_acc)
            
            return model_eval_artifact


        except Exception as e:
            raise CustomException(e, sys)