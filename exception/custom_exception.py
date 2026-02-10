import sys
import traceback
from typing import Optional


class ValidationException(Exception):
    """Custom exception that captures error context: file, line, message, and traceback.
    
    Accepts error message (string or exception) and optional error details.
    Automatically captures stack trace information for debugging.
    """

    def __init__(self, error_message: object, error_details: Optional[object] = None):
        """Initialize exception with message and optional error details.
        
        Args:
            error_message: String message or exception object describing the error
            error_details: Optional exception or exc_info tuple for context
        """
        # Normalize message
        if isinstance(error_message, BaseException):
            norm_msg = str(error_message)
        else:
            norm_msg = str(error_message)
        
        exc_type = exc_value = exc_tb = None
        
        # Extract exception info from error_details or current context
        if error_details is None:
            exc_type, exc_value, exc_tb = sys.exc_info()
        else:
            try:
                if isinstance(error_details, tuple) and len(error_details) == 3:
                    exc_type, exc_value, exc_tb = error_details
                elif isinstance(error_details, BaseException):
                    exc_type = type(error_details)
                    exc_value = error_details
                    exc_tb = getattr(error_details, '__traceback__', None)
                else:
                    exc_type, exc_value, exc_tb = sys.exc_info()
            except Exception:
                exc_type, exc_value, exc_tb = sys.exc_info()
        
        # Walk traceback to find innermost frame (actual error location)
        last_tb = exc_tb
        while last_tb and getattr(last_tb, 'tb_next', None):
            last_tb = last_tb.tb_next
        
        # Extract file and line info from innermost frame
        self.file_name = last_tb.tb_frame.f_code.co_filename if last_tb else "<unknown>"
        self.lineno = last_tb.tb_lineno if last_tb else -1
        self.error_message = norm_msg
        
        # Capture full traceback
        if exc_type and exc_tb:
            self.traceback_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
        else:
            self.traceback_str = ''
        
        super().__init__(self.__str__())
    
    def __str__(self) -> str:
        """Return formatted error message with file, line, and traceback."""
        base = f"Error in [{self.file_name}] at line [{self.lineno}] | Message: {self.error_message}"
        if self.traceback_str:
            return f"{base}\nTraceback:\n{self.traceback_str}"
        return base
    
    def __repr__(self) -> str:
        """Return developer-friendly representation."""
        return f"ValidationException(file={self.file_name!r}, line={self.lineno}, message={self.error_message!r})"
    
    def to_dict(self) -> dict:
        """Serialize exception to dictionary for logging/serialization.
        
        Returns:
            Dict with keys: file, line, message, traceback
        """
        return {
            "file": self.file_name,
            "line": self.lineno,
            "message": self.error_message,
            "traceback": self.traceback_str,
        }
