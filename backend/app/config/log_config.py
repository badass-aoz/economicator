import logging
import os
from logging.handlers import RotatingFileHandler

# Define basic configuration
LOG_DIR = "logs"
LOG_FILE = "application.log"
MAX_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5  # Keep 5 old log files

# TODO: highpri - not all logs are in the log file


def setup_logging(log_level="WARNING"):
    # Ensure the logs directory exists
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    log_file_path = os.path.join(LOG_DIR, LOG_FILE)

    # Create a logger
    logger = logging.getLogger()

    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Create a console handler and set level and formatter
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Create a file handler and set level and formatter
    file_handler = RotatingFileHandler(
        log_file_path, maxBytes=MAX_LOG_FILE_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info("Logging is set up.")
