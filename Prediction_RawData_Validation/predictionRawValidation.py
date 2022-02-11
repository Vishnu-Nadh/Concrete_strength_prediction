import os
import re
import shutil
import json
import pandas as pd
import logging
from datetime import datetime

from application_logger.loggerConfigure import configure_logger

logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Prediction_Logs/PredictionRawValidation.log")


class Prediction_Raw_Validation:
    """this class validate the prediction data and send the response"""

    def __init__(self, path):
        self.filePath = path
        self.schema_path = "data_validation_Schemas/prediction_schema.json"

    def getValuesFromSchema(self):
        """This method extracts all the relevant information from the pre-defined "Schema" file.
        Output: column_names, Number of Columns
        """
        try:
            with open(self.schema_path) as f:
                schema_dic = json.load(f)
                f.close()
            logger.info("starting getValuesFromScheama...")
            numberOfColumns = schema_dic["NumberofColumns"]
            columnNames = schema_dic["ColName"]
            logger.info("Extracted values from schema")

        except ValueError:
            logger.exception(f"Error : {ValueError}")
            raise ValueError

        except KeyError:
            logger.exception(f"Error : {KeyError}")
            raise KeyError

        except Exception as e:
            logger.exception(f"Error occured : {e}")
            raise e

        return numberOfColumns, columnNames

    def validateColumnNumber(self, numberOfColumns):
        """this method validate the number of columns in the input data"""
        try:
            data = pd.read_csv(self.filePath)
            if data.shape[1] == numberOfColumns:
                logger.info("data column number validation succeeded")
                return True
            else:
                logger.info("data column number validation failed")
                return False

        except Exception as e:
            logger.exception(f"{e}")
            raise e

    def validateColumnNames(self, columnNames):
        """this method validate the name of the columns in order

        Args:
            columnNames (dictionary): dictionary of column names as key and datatype as values
        """
        try:
            column_names = list(columnNames.keys())
            data = pd.read_csv(self.filePath)
            data_columns = data.columns
            count = 0
            for index in range(len(column_names)):
                if column_names[index] != data_columns[index]:
                    count += 1
                    logger.info(f"data failed column name validation at column number:{index + 1}")
                    break
                
            if count == 0:
                logger.info(f"data passed column name validation")
                return True
            else:
                return False
        
        except Exception as e:
            logger.exception(f"{e}")
            raise e
        
    def validateMissingValueInWholeColumn(self):
        """this method check weather any column has all missing values
        """
        try:
            data = pd.read_csv(self.filePath)
            count = 0
            for column in data.columns:
                if data[column].isnull().sum() == data.shape[0]:
                    count += 1
                    break
            if count == 0:
                logger.info("data has no column with all null values")
                return True
            else:
                logger.info("found a column with all null values in data!")
                return False
        
        except Exception as e:
            logger.exception(f"{e}")
            raise e
        