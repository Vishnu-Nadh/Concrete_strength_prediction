from operator import index
import pandas as pd
import numpy as np
import pickle
from Data_Preprocessing.preprocessData import Preprocessor

import logging
from application_logger.loggerConfigure import configure_logger


logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Prediction_Logs/predictOutputData.log")


class Predict_Output:
    """this class predict the compressive strength of the prediction data"""

    def __init__(self):
        self.logger = logger
        self.csv_path = "Prediction_Input/prediction_data.csv"
        self.model_dir = "Models/XGB_Model/XGB_Model.pickle"

    def predictFromValues(self, data):
        try:
            model = pickle.load(open(self.model_dir, "rb"))
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
            self.logger.info("null column details identified")
            data_fillna = preprocessor.fillAllNanValues()
            self.logger.info("all null values are imputed")
            data_logtr = preprocessor.LogTransformData(data_fillna)
            self.logger.info("applied logtransformation on data")
            data_scaled = preprocessor.standeredScalePredData(data_logtr)
            self.logger.info("applied standered scaling on data")
            
            # predicting output
            model = pickle.load(open(self.model_dir, "rb"))
            prediction = model.predict(data_scaled)
            
            # appending predicted value to original data
            data["Predicted_Compressive_Strength"] = prediction
            data.to_csv("Predicted_Output/predictions.csv", index=False)
            
            
            return "predicted data saved to directory"
                
        
        except Exception as e:
            logger.exception(f"Error during prediction from csv file : {e}")        
            raise e
        