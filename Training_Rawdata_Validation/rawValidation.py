import os
import shutil
import json
import pandas as pd
import logging

from application_logger.loggerConfigure import configure_logger

logger = logging.getLogger(__name__)
logger = configure_logger(logger, "rawValidation.log")


class RawData_Validation:

    """This class shall be used for handling all the validation done on the Raw Training Data!!."""

    def __init__(self, path):
        self.Batch_Directory = path
        self.schema_path = "data_validation_Schemas/training_schema.json"

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

    def deleteExistingGoodDataDirectory(self):
        """this function deletes the good data directory
        to remove old good data before starting new validation
        """
        try:
            logger.info("Entered to deleteExistingGoodDataDirectory function")
            folderPath = "training_Data_Validated/"
            if os.path.isdir(folderPath + "GoodData/"):
                shutil.rmtree(folderPath + "GoodData/")
            logger.info("deleted Good data directory")

        except OSError:
            logger.exception(f"OS Error occured :{OSError}")
            raise OSError

    def deleteExistingBadDataDirectory(self):
        """this function deletes the bad data directory
        to remove old bad data before starting new validation
        """
        try:
            logger.info("Entered to deleteExistingBadDataDirectory function")
            folderPath = "training_Data_Validated/"
            if os.path.isdir(folderPath + "BadData/"):
                shutil.rmtree(folderPath + "BadData/")
            logger.info("deleted Bad data directory")

        except OSError:
            logger.exception(f"OS Error occured :{OSError}")
            raise OSError

    def createGoodAndBadDataDirectory(self):
        """this function create good and bad data directory for saving validated input data"""
        try:
            logger.info("starting to create good and bad data directory..")
            path = os.path.join("training_data_validated/", "GoodData/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("training_data_validated/", "BadData/")
            if not os.path.isdir(path):
                os.makedirs(path)
            logger.info("Created good new and bad data directory!")

        except OSError:
            logger.exception(
                f"Error during creating good and bad data folder : {OSError}"
            )
            raise OSError

    def validateColumnLength(self, numberOfColumns):

        """This function validates the number of columns in the csv files.
        It is should be same as given in the schema file.
        If not same file is not suitable for processing and thus is moved to Bad Raw Data folder.
        If the column number matches, file is kept in Good Raw Data for processing."""

        self.deleteExistingGoodDataDirectory()
        self.deleteExistingBadDataDirectory()
        try:
            self.createGoodAndBadDataDirectory()
            logger.info("stating column length validation...")
            for csv in os.listdir(self.Batch_Directory):
                data = pd.read_csv(os.path.join(self.Batch_Directory, csv))
                if data.shape[1] == numberOfColumns:
                    shutil.copy(
                        os.path.join(self.Batch_Directory, csv),
                        "training_Data_Validated/GoodData",
                    )
                    logger.debug(
                        f"file {csv} succeeded column number validation. file copied to bad good data folder"
                    )
                else:
                    shutil.copy(
                        os.path.join(self.Batch_Directory, csv),
                        "training_Data_Validated/BadData",
                    )
                    logger.debug(
                        f"file {csv} failed column number validation. file copied to bad data folder"
                    )

        except Exception as e:
            logger.exception(f"Error while column length validation : {e}")
            raise e

    def validateColumnNames(self, columnNames):
        try:

            logger.info("starting column names validation...")
            column_names = list(columnNames.keys())
            print(column_names)
            for data in os.listdir("training_Data_Validated/GoodData/"):
                df = pd.read_csv(
                    os.path.join("training_Data_Validated/GoodData/", data)
                )
                data_columns = df.columns
                count = 0
                for index in range(len(column_names)):
                    if column_names[index] != data_columns[index]:
                        count += 1
                        shutil.move(
                            "training_Data_Validated/GoodData/" + data,
                            "training_Data_Validated/BadData",
                        )
                        logger.debug(
                            f"file {data} failed column name validation at column number:{index + 1}. file moved to bad data folder"
                        )
                        break

                if count == 0:
                    logger.debug(f"file {data} passed column name validation")

        except OSError:
            logger.exception(f"OSError during column name validation : {OSError}")
            raise OSError

        except Exception as e:
            logger.exception(f"Error during column name validation : {e}")
            raise e

    def validateMissingValuesInWholeColumn(self):
        """this function validate whether any column in dataset has all values null"""
        try:
            logger.info("started validating missing value in whole column...")
            for data in os.listdir("training_Data_Validated/GoodData/"):
                df = pd.read_csv(
                    os.path.join("training_Data_Validated/GoodData/", data)
                )
                count = 0
                for column in df.columns:
                    if df[column].isnull().sum() == df.shape[0]:
                        count += 1
                        shutil.move(
                            "training_Data_Validated/GoodData/" + data,
                            "training_Data_Validated/BadData",
                        )
                        logger.debug(
                            f"In {data} column : {column} has all values missing. file moved to bad data folder"
                        )
                        break

                if count == 0:
                    logger.debug(
                        f"{data} passed validation of missing value in all columns"
                    )

        except OSError:
            logger.exception(f"OS exception occured : {OSError}")
            raise OSError

        except Exception as e:
            logger.exception(f"Error occured : {e}")
            raise e
