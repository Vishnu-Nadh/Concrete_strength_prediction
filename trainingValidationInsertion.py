from Training_Rawdata_Validation.rawValidation import RawData_Validation
from DBoperarions.dbOperations import DB_operations
from application_logger.loggerConfigure import configure_logger
import logging
import os

logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Training_Logs/trainingValidationInsertion.log")


class Train_Validation:
    def __init__(self, path):
        self.raw_data_validation = RawData_Validation(path)
        self.dboperation = DB_operations()

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

            self.dboperation.createTableDb("Training", columnNames)
            logger.info("Table creation completed")

            # delete existing content in table before adding new data
            # Remove this 2 line of code if the data flow is continuous
            # and being replaced by new data. Else keep this line
            self.dboperation.deleteTableContentFromDB("Training")
            logger.info("Deleted table content from db before adding new data")

            self.dboperation.insertIntoTableGoodData("Training")
            logger.info("csv data inserted into database table")

            self.raw_data_validation.deleteExistingGoodDataDirectory()
            logger.info("Deleted good data folder")

            self.raw_data_validation.moveBadDataToArchiveBad()
            logger.info("bad data files moved to archived folder")

            self.raw_data_validation.deleteExistingBadDataDirectory()

            self.dboperation.selectTableFromDBintoCSV("Training")
            logger.info("databse data exported to csv succussfully")

        except Exception as e:
            logger.exception(f"Error during training data validation : {e}")
            raise e
