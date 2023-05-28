from ecp.exception import CustomException
from ecp.logger import logging
import pandas as pd
import numpy as np
import os,sys
from ecp.predictor import ModelResolver
from datetime import datetime 
from ecp.utils import load_object 


PREDICTION_DIR = 'prediction'
def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        model_resolver =ModelResolver(model_registery="saved_models")
    
        df = pd.read_csv(input_file_path)
        df.replace({'na':np.NaN},inplace=True)

        transformer = load_object(filepath=model_resolver.get_latest_transformer_path())
        target_encoder = load_object(filepath=model_resolver.get_latest_target_encoder_path())

        input_feature_names = list(transformer.feature_names_in_)

        for i in input_feature_names:
            if df[i].dtype =="object":
                df[i] = target_encoder.fit_transform(df[i])

        input_arr = transformer.transform(df[input_feature_names])

        model = load_object(filepath=model_resolver.get_latest_model_path())

        prediction = model.predict(input_arr)

        df['Prediction'] = prediction

        prediction_file_name = os.path.basename(input_file_path).replace('.csv',f"{datetime.now().strftime('%y%m%d__%h%m%s')}")

        prediction_file_name = os.path.join(PREDICTION_DIR,prediction_file_name)

        df.to_csv(prediction_file_name,index=False, header= True)

        return prediction_file_name


    except Exception as e:
        raise CustomException(e, sys)