from telnetlib import STATUS
from application_logger.loggerConfigure import configure_logger
from Prediction_RawData_Validation.predictionRawValidation import (
    Prediction_Raw_Validation,
)
import logging
import os

logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Prediction_Logs/predictionDataValidation.log")


class Predicton_Data_Validation:
    """this class does the validation of prediction csv data and sent responses"""

    def __init__(self, path):
        self.rawValidation = Prediction_Raw_Validation(path)

    def predictionCSVvalidation(self):
        """this method do all the validation and give response as dictionary of strings"""
        try:
            numberOfColumns, columnNames = self.rawValidation.getValuesFromSchema()
            logger.info("extracted schema values for validation")
            validation_dic = {"status": "success", "val_error": ""}

            if not self.rawValidation.validateColumnNumber(numberOfColumns):
                validation_dic["status"] = "error"
                validation_dic[
                    "val_error"
                ] = "Uploaded data has incorrect number of columns!"
                logger.info("column number validation failed.")

            elif not self.rawValidation.validateColumnNames(columnNames):
                validation_dic["status"] = "error"
                validation_dic[
                    "val_error"
                ] = "Uploaded data has atleast one incorrect column name"

            elif not self.rawValidation.validateMissingValueInWholeColumn():
                validation_dic["status"] = "error"
                validation_dic[
                    "val_error"
                ] = "Uploaded data has a column with all null values!"

            return validation_dic

        except Exception as e:
            logger.exception(f"{e}")
            raise e
