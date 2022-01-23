from Application_logging import logger
from Training_Rawdata_Validation.rawValidation import RawData_Validation


class Train_Validation:
    def __init__(self, path):
        self.raw_data_validation = RawData_Validation(path)
        self.file_object = open("Training_Logs/Training_Main_Log.txt", "a+")
        self.log_writer = logger.App_Logger()

    def training_data_validation(self):
        try:
            self.log_writer.log(
                self.file_object, "starting validation of data for training."
            )

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

            print("train_data_validation completed")

        except Exception as e:
            raise e
