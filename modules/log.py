import logging
import logging.handlers

LOGNAME = "argo-sensu-tools"


def get_logger(filename):
    logger = logging.getLogger(LOGNAME)
    logger.setLevel(logging.INFO)

    logfile = logging.handlers.RotatingFileHandler(
        filename, maxBytes=512 * 1024, backupCount=5
    )
    logfile.setLevel(logging.INFO)
    logfile.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(logfile)

    return logger
