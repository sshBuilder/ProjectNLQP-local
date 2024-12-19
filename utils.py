# utils.py

import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_message(level, message):
    """
    Logs a message at the specified level.
    Args:
        level (str): Log level (INFO, WARNING, ERROR).
        message (str): Message to log.
    """
    logger = logging.getLogger()
    if level.upper() == "INFO":
        logger.info(message)
    elif level.upper() == "WARNING":
        logger.warning(message)
    elif level.upper() == "ERROR":
        logger.error(message)
