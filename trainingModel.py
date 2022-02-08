"""This is the entry point to training the model """

from sklearn.model_selection import train_test_split
from Data_Ingestion.train_data_loader import Data_Loader_Train
from Data_Preprocessing.preprocessTraindata import Preprocessor
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
            
                       
                       
        except Exception as e:
            logger.exception(f"ERROR occured: {e}")
            raise e
        