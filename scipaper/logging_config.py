import logging
import sys

def setup_logging():
    """Configures the root logger for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        stream=sys.stdout,
    )
    # Get the root logger
    logger = logging.getLogger()
    # You can add handlers here if you want to log to files, etc.
    # For now, we'll just use the basic config which logs to the console.
    logger.info("Logging configured.")
