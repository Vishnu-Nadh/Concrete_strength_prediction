"""This is the entry point to training the model """
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from Data_Ingestion.train_data_loader import Data_Loader_Train
from Data_Preprocessing.preprocessData import Preprocessor
from clustering.clustering import Data_Clustering
from File_Operations.fileOperations import File_Operations
# from Best_model_finder.tuner import Model_Finder
from xgboost import XGBRegressor
import logging
from application_logger.loggerConfigure import configure_logger


logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Training_Logs/trainingModel.log")

class Train_Model:
    """this class is used to train the model using the exported data from database"""
    def __init__(self):
        self.logger = logger
    
    def trainModel(self):
        """this function train and tune the model and saves models"""
        try:
            dataloader = Data_Loader_Train()
            data = dataloader.get_train_data()
            
            # data preprocessing
            preprocessor = Preprocessor(data)
            
            is_null_present, columns_with_nan = preprocessor.getColsWithNullValues()
            
            data = preprocessor.fillAllNanValues()
            self.logger.info("imputed all missing values in data")
            
            X, y = preprocessor.splitFeatureAndLabels(data)
            self.logger.info("data features and labels saperated")

            """customised machine learning aproach (clustering aproach does not work here well
            because data set is too small to train individual algorithms on each clusters formed.
            Hence follow the ordinary aproach"""
            
            # apply log transformation
            X_logtransformed = preprocessor.LogTransformData(X)
            self.logger.info("logarithemic transformation completed")
            
            # apply standered scaler
            X_scaled = preprocessor.standeredScalingData(X_logtransformed, "Std_Scaler")
            self.logger.info("standered scaling of data completed")
            
            # splitting to train test data
            x_train, x_test, y_train, y_test = preprocessor.trainTestSplitData(X_scaled, y)
            
            # model training with tuned parameters
            params = {
                    "booster": "dart",
                    "eta": 0.4632229410828487,
                    "gamma": 7.077192780534438,
                    "max_depth": 3,
                    "subsample": 0.8092309111849526,
                    "lambda": 0.015342068089733317,
                    }

            xgb_r = XGBRegressor(**params)
            xgb_r.fit(x_train, y_train)
            self.logger.info("model training completed")
            
            fileops = File_Operations()
            fileops.saveModel(xgb_r, "XGB_Model")
            
            model = fileops.loadModel("XGB_Model")
            
            model_train_score = model.score(x_train, y_train)
            model_test_score = model.score(x_test, y_test)
            
            logger.info(f"model training completed with training_score {model_train_score} and test_score {model_test_score}")
                            
        except Exception as e:
            self.logger.exception(f"ERROR occured: {e}")
            raise e
        