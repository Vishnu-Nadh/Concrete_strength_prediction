import logging

from application_logger.loggerConfigure import configure_logger


logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Training_Logs/preprocessTrainData.log")


class Preprocessor:
    """this class do the necessary preprocessing of the training or prediction data
    and retrun the preprocessed data as the dataframe"""

    def __init__(self, data):
        self.data = data

    def preprocessTrainData(self):
        pass

    def splitFeatureAndLabels(self):
        pass

    def getColsWithNullValues(self):
        try:
            is_null_present = False
            columns_with_nan = [
                column
                for column in self.data.columns
                if self.data[column].isnull().sum() > 0
            ]
            if len(columns_with_nan) > 0:
                is_null_present = True
            logger.info(f"found null values in {len(columns_with_nan)} columns")
        except Exception as e:
            logger.exception("Error while finding columns with nan values", str(e))
            raise e

        return is_null_present, columns_with_nan
