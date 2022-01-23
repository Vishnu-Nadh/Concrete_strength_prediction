from Application_logging.logger import App_Logger
import os
import shutil
import json
import pandas as pd


class RawData_Validation:

    """This class shall be used for handling all the validation done on the Raw Training Data!!."""

    def __init__(self, path):
        self.Batch_Directory = path
        self.logger = App_Logger()
        self.schema_path = "data_validation_Schemas/training_schema.json"

    def getValuesFromSchema(self):
        """This method extracts all the relevant information from the pre-defined "Schema" file.
        Output: column_names, Number of Columns
        """
        try:
            with open(self.schema_path) as f:
                schema_dic = json.load(f)
                f.close()

            numberOfColumns = schema_dic["NumberofColumns"]
            columnNames = schema_dic["ColName"]

            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", "a+")
            self.logger.log(file, "extracted schema values successfully")
            file.close()

        except ValueError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", "a+")
            self.logger.log(
                file, "ValueError:Value not found inside schema_training.json"
            )
            file.close()
            raise ValueError

        except KeyError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", "a+")
            self.logger.log(file, "KeyError:Key value error incorrect key passed")
            file.close()
            raise KeyError

        except Exception as e:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", "a+")
            self.logger.log(file, "Error occured during get values from schema.!")
            file.close()
            raise e

        return numberOfColumns, columnNames

    def deleteExistingGoodDataDirectory(self):
        """this function deletes the good data directory
        to remove old good data before starting new validation
        """
        try:
            folderPath = "training_Data_Validated/"
            if os.path.isdir(folderPath + "GoodData/"):
                shutil.rmtree(folderPath + "GoodData/")
                f = open("Training_Logs/GeneralLogs.txt", "a+")
                self.logger.log(
                    f, "Good data folder deleted before starting of validation!"
                )
                f.close()

        except OSError:
            f = open("Training_Logs/GeneralLogs.txt", "a+")
            self.logger.log(
                f,
                "Error occured while deleting good data folder before data validation..!",
            )
            f.close()
            raise OSError

    def deleteExistingBadDataDirectory(self):
        """this function deletes the bad data directory
        to remove old bad data before starting new validation
        """
        try:
            folderPath = "training_Data_Validated/"
            if os.path.isdir(folderPath + "BadData/"):
                shutil.rmtree(folderPath + "BadData/")
                f = open("Training_Logs/GeneralLogs.txt", "a+")
                self.logger.log(
                    f, "Bad data folder deleted before starting of validation!"
                )
                f.close()

        except OSError:
            f = open("Training_Logs/GeneralLogs.txt", "a+")
            self.logger.log(
                f,
                "Error occured while deleting bad data folder before data validation..!",
            )
            f.close()
            raise OSError

    def createGoodAndBadDataDirectory(self):
        """this function create good and bad data directory for saving validated input data"""
        try:
            path = os.path.join("training_data_validated/", "GoodData/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("training_data_validated/", "BadData/")
            if not os.path.isdir(path):
                os.makedirs(path)

            f = open("Training_Logs/GeneralLogs.txt", "a+")
            self.logger.log(f, "created GoodData and BadData folder.")
            f.close()

        except OSError:
            f = open("Training_Logs/GeneralLogs.txt", "a+")
            self.logger.log(
                f, "Error occured while creating good and bad data directory !"
            )
            f.close()
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
            f = open("Training_Logs/validateColumnLengthLog.txt", "a+")
            for csv in os.listdir(self.Batch_Directory):
                data = pd.read_csv(os.path.join(self.Batch_Directory, csv))
                if data.shape[1] == numberOfColumns:
                    shutil.copy(
                        os.path.join(self.Batch_Directory, csv),
                        "training_Data_Validated/GoodData",
                    )
                    self.logger.log(
                        f,
                        f"column length validation passed {csv} moved to GoodData folder",
                    )
                else:
                    shutil.copy(
                        os.path.join(self.Batch_Directory, csv),
                        "training_Data_Validated/BadData",
                    )
                    self.logger.log(
                        f,
                        f"column length validation failed {csv} moved to BadData folder",
                    )
            f.close()

        except Exception as e:
            f = open("Training_Logs/validateColumnLengthLog.txt", "a+")
            self.logger.log(
                f, "Error occured during during validation of column number..!"
            )
            f.close()
            raise e

    def validateColumnNames(self, columnNames):
        try:
            f = open("Training_Logs/validateColumnNamesLog.txt", "a+")

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
                        self.logger.log(
                            f,
                            f"Column name validation failed. {data} moved to bad data folder!",
                        )
                        break
                if count == 0:
                    self.logger.log(f, f"{data} passed acolumn name validation")
            f.close()

        except OSError:
            f = open("Training_Logs/validateColumnNamesLog.txt", "a+")
            self.logger.log(f, "Error while moving data to bad data folder!")
            f.close()
            raise OSError

        except Exception as e:
            f = open("Training_Logs/validateColumnNamesLog.txt", "a+")
            self.logger.log(f, "Error during validation of column names..!")
            f.close()
            raise e

    def validateMissingValuesInWholeColumn(self):
        """this function validate whether any column in dataset has all values null"""
        try:
            f = open("Training_Logs/validateMissingValuesInWholeColumnLog.txt", "a+")
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
                        self.logger.log(
                            f,
                            f"missing value in whole column validation failed. {data} moved to bad data folder!",
                        )
                        break
                if count == 0:
                    self.logger.log(
                        f, f"{data} passed missing value in whole column validation"
                    )
            f.close()

        except OSError:
            f = open("Training_Logs/validateMissingValuesInWholeColumnLog.txt", "a+")
            self.logger.log(f, "Error while moving data to bad data folder!")
            f.close()
            raise OSError

        except Exception as e:
            f = open("Training_Logs/validateMissingValuesInWholeColumnLog.txt", "a+")
            self.logger.log(
                f, "Error during missing value in whole column validataion!"
            )
            f.close()
            raise e
