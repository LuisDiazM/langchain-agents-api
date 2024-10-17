import logging
from pythonjsonlogger import jsonlogger


def get_logger() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s",
    rename_fields={"levelname": "severity", "asctime": "timestamp"},)
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    return logger
