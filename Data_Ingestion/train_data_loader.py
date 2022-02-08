import pandas as pd
import logging
from application_logger.loggerConfigure import configure_logger

logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Training_Logs/train_data_loader.log")


class Data_Loader_Train:
    """this class loads the train data from folder for training"""

    def __init__(self):
        self.training_file = "Training_FileFromDB/InputFile.csv"

    def get_train_data(self):
        """this function read csv data stored in file and return a pandas dataframe"""
        try:
            data = pd.read_csv(self.training_file)
            logger.info("Training file loaded to pandas dataframe")
        except Exception as e:
            logger.exception("error while reading inputFile.csv", str(e))
            raise e

        return data
