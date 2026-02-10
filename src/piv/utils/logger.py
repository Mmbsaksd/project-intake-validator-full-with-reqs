import os
import logging
import time
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone

DEFAULT_LOG_DIR = os.path.join(os.getcwd(), "logs")


def _ensure_dir(path: str):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        # best-effort: if directory creation fails, logging will fall back to console
        pass


def get_logger(name: str = __name__, log_dir: str = DEFAULT_LOG_DIR, level=logging.INFO):
    """Return a configured standard-library logger.

    - Rotating file handler writing to `log_dir` with timestamped filename.
    - Console handler with the same formatter.
    Designed to be idempotent: calling repeatedly for the same `name` returns
    the same configured logger.
    """
    logger = logging.getLogger(name)
    if getattr(logger, "_configured_by_utils", False):
        return logger

    logger.setLevel(level)

    _ensure_dir(log_dir)
    # Use UTC for file timestamps to make logs consistent across hosts
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(log_dir, f"app_{timestamp}.log")

    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    datefmt = "%Y-%m-%dT%H:%M:%S%z"
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    # Force formatter to use UTC/GMT times (so %z is +0000)
    formatter.converter = time.gmtime

    try:
        file_handler = RotatingFileHandler(filename, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        # If file handler cannot be created, continue with console only
        pass

    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # mark configured
    logger._configured_by_utils = True
    return logger
