import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


DEFAULT_LOG_DIR = "logs"
DEFAULT_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(funcName)s: %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


_LEVEL_NAMES = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARN": logging.WARNING,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}

logger = logging.getLogger()

def info(msg):
    logger.log(logging.INFO, msg, stacklevel=2)
def warning(msg):
    logger.log(logging.WARNING, msg, stacklevel=2)
def error(msg):
    logger.log(logging.ERROR, msg, stacklevel=2)
def debug(msg):
    logger.log(logging.DEBUG, msg, stacklevel=2)


class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level):
        super().__init__()
        self.max_level = max_level

    def filter(self, record):
        return record.levelno <= self.max_level


def _get_level(level):
    if isinstance(level, int):
        return level

    level_name = str(level).upper()
    if level_name not in _LEVEL_NAMES:
        raise ValueError(f"unsupported log level: {level}")
    return _LEVEL_NAMES[level_name]


def setup_logger(
    name="futu-api",
    log_dir=DEFAULT_LOG_DIR,
    level="INFO",
    filename=None,
    console=True,
    max_bytes=10 * 1024 * 1024,
    backup_count=5,
):
    """Create a logger that writes to console and a rotating log file."""
    log_level = _get_level(level)
    #logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    if filename is None:
        filename = f"{name}.log"

    formatter = logging.Formatter(DEFAULT_LOG_FORMAT, DEFAULT_DATE_FORMAT)

    file_handler = RotatingFileHandler(
        log_path / filename,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if console:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(log_level)
        stdout_handler.addFilter(MaxLevelFilter(logging.WARNING))
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)

        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(max(log_level, logging.ERROR))
        stderr_handler.setFormatter(formatter)
        logger.addHandler(stderr_handler)

    return logger

def init():
    return setup_logger(name="timer", log_dir="logs", level="DEBUG")