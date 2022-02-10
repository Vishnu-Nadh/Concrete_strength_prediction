import logging
# from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import pickle
from File_Operations.fileOperations import File_Operations

from application_logger.loggerConfigure import configure_logger

logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Prediction_Logs/preprocessPredValues.log")

class PreprocessVals:
    """this class is used to preprocess the prediction data values"""
    def __init__(self, data):
        self.data = data

    def preprocessPredvalues(self):
        """this method completes the preprocessing of the input prediction values
        """
        try:
            data_transformed = self.logTransformPredvalues()
            data_scaled = self.standeredScalePredValues(data_transformed)
            logger.info(f"prediction input values data preprocessing completed")
            return data_scaled
        except Exception as e:
            logger.exception(f"{e}")
            raise e
        
    def logTransformPredvalues(self):
        """this method is used for log transformation of the dataframe
        """
        try:
            data_transformed = self.data.apply(lambda x:np.log1p(x), axis=1)
            logger.info("input prediction values are logtransformed")
            return data_transformed
        except Exception as e:
            logger.exception(f"LogTransformation Error : {e}")
            raise e
        
    def standeredScalePredValues(self, data):
        """this method scale the input prediction values
        """
        try:
            scaler = pickle.load(open("Scaler/Std_Scaler/Std_Scaler.sav", "rb"))
            data_scaled = pd.DataFrame(scaler.transform(data), columns=data.columns)
            logger.info(f"prediction data values scaled")
            return data_scaled
        
        except Exception as e:
            logger.exception(f"Error while standered scaling {e}")
            raise e
        