from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV

import logging
from application_logger.loggerConfigure import configure_logger


logger = logging.getLogger(__name__)
logger = configure_logger(logger, "Training_Logs/tuningModel.log")


class Model_Finder:
    """this class finds the best model for the given cluster based on accuracy after parameter tuning"""

    def __init__(self):
        self.xgb = XGBRegressor()
        self.ridge = Ridge()
        self.rf = RandomForestRegressor()

    def findBestModel(self, x_train, y_train, x_test, y_test):
        try:
            # xgboost regression
            best_params_for_xgb = self.findBestParamsForXGB(x_train, y_train)
            # print(best_params_for_xgb)
            xgb = XGBRegressor(**best_params_for_xgb)
            xgb.fit(x_train, y_train)
            xgb_score = xgb.score(x_test, y_test)

            # random forest regression

            # print(f"xgb_score {xgb_score}")

            # compare the accuracy of all model

            # select and return the best model with tuned parameter

            return xgb

        except Exception as e:
            raise e

    def findBestParamsForXGB(self, x_train, y_train):
        """this function find the best parameters for the xgbregressor algorithms after parameter tuning
        return model object with tuned parameter

        Args:
            x_train (dataframe): features for training
            y_train (dataframe): labels
        """
        try:
            self.search_params_for_xgb = {
                "booster": ["dart", "gbtree"],
                "eta": [0.3, 0.463, 0.5],
                "gamma": [5, 7, 9],
                "max_depth": [2, 3, 6],
                "subsample": [0.809, 1],
                "lambda": [0.01, 0.01534],
            }

            xgb = XGBRegressor()
            GS = GridSearchCV(xgb, self.search_params_for_xgb)
            GS.fit(x_train, y_train)
            best_params_for_xgb = GS.best_params_
            logger.info("Found best params for xgboost regressor")
            return best_params_for_xgb

        except Exception as e:
            pass

            raise e

    def findBestParamsForRidge(self):
        pass

    def findBestParamsForRF(self):
        pass
