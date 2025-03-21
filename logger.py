import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('mail_work_logger')

logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler('./log_files/details.log')
file_handler.setLevel(logging.DEBUG)

# Rotating file handler
rotatingFileHandler = RotatingFileHandler(
    "log_files/details.log",
    maxBytes=1024*1024,
    backupCount=20
)

# Define log message format
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
rotatingFileHandler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(rotatingFileHandler)
