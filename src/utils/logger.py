import logging
import os
from datetime import datetime
from src.config import LOG_DIRERCTORY


def setup_logger(name: str = None, log_to_console: bool = True, log_level: str = "INFO") -> logging.Logger:
    """
    Sets up and returns a configured logger.

    This function creates a logger with a file handler that writes to a daily rotating log file.
    Optionally, it can also add a console handler. It ensures handlers are only added once to avoid duplicates.

    Args:
        name (str, optional): Name of the logger. If None, the root logger is used. Defaults to None.
        log_to_console (bool, optional): Whether to also log to the console. Defaults to True.
        log_level (str, optional): Logging level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
                                   Defaults to 'INFO'.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Ensure the log directory exists
    os.makedirs(LOG_DIRERCTORY, exist_ok=True)

    # Construct log file path
    log_filename = os.path.join(
        LOG_DIRERCTORY,
        f"app_log_{datetime.now().strftime('%Y-%m-%d')}.log"
    )

    # Get the logger
    logger = logging.getLogger(name)

    if not logger.handlers:
        # Set log level
        logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # File handler
        file_handler = logging.FileHandler(log_filename, mode='a')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Optional console handler
        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger
