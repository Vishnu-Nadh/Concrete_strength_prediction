import logging
import os


def configure_logger(logger, logfile_name, log_level=logging.DEBUG):
    logger.setLevel(log_level)
    logging_str = "[%(asctime)s : %(levelname)s : %(module)s] - %(message)s"
    formatter = logging.Formatter(logging_str)

    logging_dir = "App_running_Logs"
    os.makedirs(logging_dir, exist_ok=True)
    trainlog_dir = os.path.join(logging_dir, "Training_Logs")
    os.makedirs(trainlog_dir, exist_ok=True)
    predictionlog_dir = os.path.join(logging_dir, "Prediction_Logs")
    os.makedirs(predictionlog_dir, exist_ok=True)
    generallog_dir = os.path.join(logging_dir, "General_Logs")
    os.makedirs(generallog_dir, exist_ok=True)

    logging_file = os.path.join(logging_dir, logfile_name)
    file_handler = logging.FileHandler(logging_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger
