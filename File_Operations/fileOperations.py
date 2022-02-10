from asyncio.log import logger
import pickle
import os
import shutil
import logging
from application_logger.loggerConfigure import configure_logger


logger = logging.getLogger(__name__)
logger = configure_logger(logger, "General_Logs/fileOpertions.log")


class File_Operations:
    """this class is used fof file operations such as saving, loading and finding of model files"""

    def __init__(self):
        self.logger = logger
        self.model_dir = "Models/"
        self.scaler_dir = "Scaler/"

    def saveModel(self, model, filename):
        """this function saves the model file with the filename given in the models directory

        Args:
            model (python object): trained ML model
            filename (string): filename in which model is to be saved
        """
        try:
            path = os.path.join(
                self.model_dir, filename
            )  # create seperate directory for each cluster
            if os.path.isdir(
                path
            ):  # remove previously existing models for each clusters
                shutil.rmtree(self.model_dir)
                os.makedirs(path)
            else:
                os.makedirs(path)

            with open(path + "/" + filename + ".pickle", "wb") as f:
                pickle.dump(model, f)  # save the model to file

            self.logger.info(f"model {filename} saved to model directory")

            return "success"

        except Exception as e:
            self.logger.exception(f"{e}")
            raise e

    def saveScaler(self, scaler, filename):
        """this function saves the scaler file with the filename given in the scalers directory

        Args:
            scaler (python object): trained ML scaler
            filename (string): filename in which scaler is to be saved
        """
        try:
            path = os.path.join(
                self.scaler_dir, filename
            )  # create seperate directory for each cluster
            if os.path.isdir(
                path
            ):  # remove previously existing scalers for each clusters
                shutil.rmtree(self.scaler_dir)
                os.makedirs(path)
            else:
                os.makedirs(path)

            with open(path + "/" + filename + ".sav", "wb") as f:
                pickle.dump(scaler, f)  # save the scaler to file

            self.logger.info(f"scaler {filename} saved to scaler directory")

            return "success"

        except Exception as e:
            self.logger.exception(f"{e}")
            raise e

    def loadModel(self, model_name):
        """this method load the model for prediction from the saved location of pickle file

        Args:
            model_name (string): model name 
        """
        
        try:
            
            file_path = os.path.join(self.model_dir + model_name, model_name + ".pickle")
            model = pickle.load(open(file_path, "rb"))
            logger.info("loaded model from saved pickle format")
            
            return model
        
        except Exception as e:
            logger.exception(f"{e}")
            pass
        
            raise e
                     