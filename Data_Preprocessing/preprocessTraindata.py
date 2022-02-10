from ast import Try
import imp
import logging
from re import X
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import pickle
from File_Operations.fileOperations import File_Operations


from application_logger.loggerConfigure import configure_logger


logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Training_Logs/preprocessTrainData.log")


class Preprocessor:
    """this class do the necessary preprocessing of the training or prediction data
    and retrun the preprocessed data as the dataframe"""

    def __init__(self, data):
        self.data = data

    def splitFeatureAndLabels(self, data):
        """saparate the labels and features and return two dataframe X, y respectively.

        Args:
            data (dataframe): input dataframe to be saparated
        """
        try:
            X = data.drop("Concrete_compressive_strength", axis=1)
            y = data["Concrete_compressive_strength"]
            logger.info("data saparated to features and labels")
        except Exception as e:
            logger.exception(f"error while saparating features and labels {e}")
            raise e

        return X, y

    def getColsWithNullValues(self):
        try:
            is_null_present = False
            columns_with_nan = [
                column
                for column in self.data.columns
                if self.data[column].isnull().sum() > 0
            ]
            if len(columns_with_nan) > 0:
                is_null_present = True
            logger.info(f"found null values in {len(columns_with_nan)} columns")
        except Exception as e:
            logger.exception("Error while finding columns with nan values", str(e))
            raise e

        return is_null_present, columns_with_nan

    def fillAllNanValues(self):
        """this method fills all the null values in the dataframe using knn imputation"""

        try:
            imputer = KNNImputer(
                n_neighbors=3, weights="uniform", missing_values=np.nan
            )
            data = pd.DataFrame(
                imputer.fit_transform(self.data), columns=self.data.columns
            )
            logger.info("imputed all missing value in the data")

        except Exception as e:
            logger.exception(f"error in missing value imputation : {e}")
            raise e

        return data
    
    def standeredScalingData(self, X, filename=None):
        """apply the standered scaling to the features data and return as dataframe

        Args:
            X (dataframe): input feature data
        """
        try:
            scaler = StandardScaler()
            scaler.fit(X)
            
            if filename != None:
                # SAVING SCALER FOR PREDICTION DATA
                fileop = File_Operations()
                fileop.saveScaler(scaler, filename)
                logger.info(f"{filename} scaler saved in directory")

            X_tr = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
            logger.info("training data is scaled using standered scaler")
                    
            return X_tr    
            
        except Exception as e:
            logger.exception(f"{e}")
            raise e
        
    def LogTransformData(self, data):
        """this method apply the log transformation to the data passed in 
        returns : logarithmic transformed data

        Args:
            data (dataframe): input data of features
        """
        try:
            data_transformed = data.apply(lambda x:np.log1p(x), axis=1)
            logger.info("applied logarithamic transformation to the data") 
            return data_transformed
        
        except Exception as e:
            logger.exception(f"Error while logarithmic transformation {e}")    
            raise e
        
    def trainTestSplitData(self, X, y):
        """this function do the train test split of the d=given features and labels

        Args:
            X (dataframe): features data
            y (dataframe): labels data
            
        """
        try:
            x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)
            logger.info("data splitted to train and test data sets")
            return x_train, x_test, y_train, y_test
        
        except Exception as e:
            logger.exception(f"{e}")
            raise e
        