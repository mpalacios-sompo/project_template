from src.utils.logger import setup_logger


if __name__ == "__main__":

    logger = setup_logger(__name__)
    logger.info("My log message")
    
    print("This is a placeholder for the main script.")