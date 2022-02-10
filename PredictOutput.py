from asyncio.log import logger
import pandas as pd
import numpy as np
import pickle

import logging
from application_logger.loggerConfigure import configure_logger


logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Training_Logs/preprocessTrainData.log")


class Predict_Output:
    """this class predict the compressive strength of the prediction data"""

    def __init__(self):
        self.logger = logger

    def predictFromValues(self, data):
        try:
            model = pickle.load(open("Models/XGB_Model/XGB_Model.pickle", "rb"))
            prediction = model.predict(data)[0]
            self.logger.info(f"predicted the compressive strength as {prediction}")
            return prediction

        except Exception as e:
            self.logger.exception(f"error while predicting output : {e}")
            raise e
    
    def predictFromCSV(self, data):
        """this method predict output from the csv data after preprocessing the data

        Args:
            data (data): input features data
        """
        try:
            # preprocessing steps goes here
            pass
        
        except Exception as e:
            pass
        
            raise e
        