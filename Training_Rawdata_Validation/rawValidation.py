import os
import shutil
import json
from matplotlib import container
import pandas as pd
import logging
from datetime import datetime

from application_logger.loggerConfigure import configure_logger

logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Training_Logs/rawValidation.log")


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
            path = os.path.join("training_Data_Validated/", "GoodData/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("training_Data_Validated/", "BadData/")
            if not os.path.isdir(path):
                os.makedirs(path)
            logger.info("Created good new and bad data directory!")

        except OSError:
            logger.exception(
                f"Error during creating good and bad data folder : {OSError}"
            )
            raise OSError

    def moveBadDataToArchiveBad(self):
        """this function move the bad files from bad data folder ot archive bad folder"""
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H%M%S")

        try:

            src = "training_Data_Validated/BadData/"
            if os.path.isdir(src):
                path = "Training_ArchivedBadData"
                if not os.path.isdir(path):
                    os.makedirs(path)
                filepath = (
                    "Training_ArchivedBadData/Bad_data_" + str(date) + "_" + str(time)
                )

                if not os.path.isdir(filepath):
                    os.makedirs(filepath)
                files = os.listdir(src)
                for f in files:
                    if f not in os.listdir(filepath):
                        shutil.move(src + f, filepath)
                logger.info("Bad file moved to archive bad data folder")
                path = "training_Data_Validated/"
                if os.path.isdir(path + "BadData/"):
                    shutil.rmtree(path + "BadData/")
                logger.info("bad data folder deleted succussfully")

            # the code to remove the datas from archived data folder assuming that
            # every data stored there is being redirected to client side within a perticular
            # piriod. This is to avoid unnesessary aggragation of datas in that folder which
            # would take up space in heroku container

            files = os.listdir("Training_ArchivedBadData/")
            if len(files) > 3:
                old_files = files[0 : (len(files) - 3)]
                for file in old_files:
                    old_path = os.path.join("Training_ArchivedBadData", file)
                    shutil.rmtree(old_path)
                logger.info("Excessive files from Training_ArchivedBadData removed")

        except Exception as e:
            logger.exception(f"error while moving bad files to archive bad folder: {e}")
            raise e

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
                        "training_Data_Validated/GoodData/",
                    )
                    logger.debug(
                        f"file {csv} succeeded column number validation. file copied to good data folder"
                    )
                else:
                    shutil.copy(
                        os.path.join(self.Batch_Directory, csv),
                        "training_Data_Validated/BadData/",
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
            raise
