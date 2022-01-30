from Training_Rawdata_Validation.rawValidation import RawData_Validation
from application_logger.loggerConfigure import configure_logger
import logging
import os

logger = logging.getLogger(__name__)
logger = configure_logger(logger, "trainingValidationInsertion.log")


class Train_Validation:
    def __init__(self, path):
        self.raw_data_validation = RawData_Validation(path)

    def training_data_validation(self):
        try:
            logger.info("training data validation started...!")
            # get the values for validation of the data
            (
                numberOfColumns,
                columnNames,
            ) = self.raw_data_validation.getValuesFromSchema()

            # validationg totel number of columns in the training data
            self.raw_data_validation.validateColumnLength(numberOfColumns)

            # validating column names
            self.raw_data_validation.validateColumnNames(columnNames)

            # validating missing values in the whole column
            self.raw_data_validation.validateMissingValuesInWholeColumn()
            logger.info("Training data validation completed!")

        except Exception as e:
            logger.exception(f"Error during training data validation : {e}")
            raise e
