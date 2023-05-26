from ecp.entity import artifact_entity,config_entity
from ecp.exception import CustomException
from ecp.logger import logging
import sys
from sklearn.linear_model import LogisticRegression 
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier 
from ecp import utils
from sklearn.metrics import accuracy_score


class ModelTrainer:
    def __init__(self,data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                model_trainer_config:config_entity.ModelTrainerConfig):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys)
    
    def train_model(self,x,y):
        try:
            rfc = RandomForestClassifier(n_estimators=100)
            rfc.fit(x,y)
            return rfc
        except Exception as e:
            raise CustomException(e, sys)


    def initiate_model_trainer(self)->artifact_entity.ModelTrainerArtifact:
        try:
            train_arr = utils.load_numpy_array_data(filepath=self.data_transformation_artifact.transform_train_path)
            test_arr = utils.load_numpy_array_data(filepath=self.data_transformation_artifact.transform_test_path) 

            # logging.info(f"{train_arr[:3,:]}")

            x_train , y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            model = self.train_model(x=x_train,y=y_train)

            y_pred_train = model.predict(x_train)
            accuracy_train_score = accuracy_score(y_train,y_pred_train)

            y_pred_test = model.predict(x_test)

            accuracy_test_score = accuracy_score(y_test,y_pred_test)

            logging.info(f" test accuracy is {accuracy_test_score}")

            if accuracy_test_score < self.model_trainer_config.expected_accuracy:
                raise Exception(f"Model is not good as it gave less accuracy form expectation which is {accuracy_test_score} ")

            diff = (accuracy_train_score - accuracy_test_score)

            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Model is over fitted with train and test diff : {diff} ")
            
            utils.save_object(filepath=self.model_trainer_config.model_path,obj=model)

            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(
                model_path=self.model_trainer_config.model_path,
                accuracy_train_score =accuracy_train_score,
                accuracy_test_score = accuracy_test_score
                )

            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e, sys)
