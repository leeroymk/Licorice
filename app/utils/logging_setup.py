import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    log_handler = RotatingFileHandler("logs.log", maxBytes=10 * 1024 * 1024, backupCount=5)
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y.%m.%d %H:%M:%S"
    )
    log_handler.setFormatter(formatter)

    logging.getLogger().addHandler(log_handler)
    logging.getLogger().setLevel(logging.INFO)

    return log_handler
