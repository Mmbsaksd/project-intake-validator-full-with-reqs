import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone
import time


class CustomLogger:
    """Custom logger with file and console output, rotating file handler.
    
    Creates single consolidated app.log in configurable directory.
    Uses both file (rotating) and console handlers for comprehensive logging.
    """

    def __init__(self, log_dir="logs"):
        """Initialize logger with directory setup.
        
        Args:
            log_dir: Directory to store log files (relative to cwd)
        """
        self.logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Use single fixed log filename - RotatingFileHandler will manage rotation
        self.log_file_path = os.path.join(self.logs_dir, "app.log")

    def get_logger(self, name=__name__):
        """Get configured logger with file and console handlers.
        
        Args:
            name: Logger name (typically __name__ or module path)
            
        Returns:
            Configured standard library logger
        """
        logger_name = os.path.basename(name) if '/' in name or '\\' in name else name
        
        # Create/get logger
        logger = logging.getLogger(logger_name)
        
        # Skip if already configured to avoid duplicate handlers
        if hasattr(logger, '_custom_configured'):
            return logger
        
        logger.setLevel(logging.INFO)
        
        # Format: YYYY-MM-DD HH:MM:SS | LEVEL | message
        fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
        # Force UTC timestamps
        formatter.converter = time.gmtime
        
        # File handler with rotation (5MB per file, keep 5 backups)
        try:
            file_handler = RotatingFileHandler(
                self.log_file_path,
                maxBytes=5 * 1024 * 1024,  # 5 MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception:
            # Fallback to console-only if file handler fails
            pass
        
        # Console handler (stderr)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Mark as configured
        logger._custom_configured = True
        
        return logger
