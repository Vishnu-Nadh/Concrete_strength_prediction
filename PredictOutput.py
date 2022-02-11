import pandas as pd
import numpy as np
import pickle
from Data_Preprocessing.preprocessData import Preprocessor

import logging
from application_logger.loggerConfigure import configure_logger


logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Prediction_Logs/preprocessPredData.log")


class Predict_Output:
    """this class predict the compressive strength of the prediction data"""

    def __init__(self):
        self.logger = logger
        self.csv_path = "Prediction_Input/prediction_data.csv"

    def predictFromValues(self, data):
        try:
            model = pickle.load(open("Models/XGB_Model/XGB_Model.pickle", "rb"))
            prediction = model.predict(data)[0]
            self.logger.info(f"predicted the compressive strength as {prediction}")
            return prediction

        except Exception as e:
            self.logger.exception(f"error while predicting output : {e}")
            raise e
    
    def predictFromCSV(self):
        """this method predict output from the csv data after preprocessing the data

        Args:
            data (data): input features data
        """
        try:
            data = pd.read_csv(self.csv_path)
            # preprocessing steps goes here
            preprocessor = Preprocessor(data, "Prediction_Logs/preprocessPreditionCSV.log")
            is_null_present, columns_with_nan = preprocessor.getColsWithNullValues()
            print(columns_with_nan)
            data = preprocessor.fillAllNanValues()
            print(data.isnull().sum())
            data = preprocessor.LogTransformData(data)
            print(f"log-transformed : {data.head()}")
            data_scaled = preprocessor.standeredScalePredData(data)
            print(f"scaled data {data_scaled.head()}")
            
            return data_scaled
                
        
        except Exception as e:
            logger.exception(f"Error during prediction from csv file : {e}")        
            raise e
        