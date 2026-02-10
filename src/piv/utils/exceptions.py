import sys
import traceback
from typing import Optional


class ResearchAnalystException(Exception):
    """Application-level exception that captures origin filename, line number and traceback.

    Accepts either a message string or an exception instance as `error_message`. Optionally an
    `error_details` object can be provided (e.g., an ``exc_info`` tuple or another exception).
    """
    def __init__(self, error_message: object, error_details: Optional[object] = None):
        # Normalize message
        if isinstance(error_message, BaseException):
            norm_msg = str(error_message)
        else:
            norm_msg = str(error_message)

        exc_type = exc_value = exc_tb = None

        if error_details is None:
            exc_type, exc_value, exc_tb = sys.exc_info()
        else:
            # If user passed an exc_info-like object
            try:
                if isinstance(error_details, tuple) and len(error_details) == 3:
                    exc_type, exc_value, exc_tb = error_details
                elif isinstance(error_details, BaseException):
                    exc_type, exc_value, exc_tb = type(error_details), error_details, error_details.__traceback__
                else:
                    exc_type, exc_value, exc_tb = sys.exc_info()
            except Exception:
                exc_type, exc_value, exc_tb = sys.exc_info()

        # Walk to last frame
        last_tb = exc_tb
        while last_tb and getattr(last_tb, "tb_next", None):
            last_tb = last_tb.tb_next

        self.file_name = last_tb.tb_frame.f_code.co_filename if last_tb else "<unknown>"
        self.lineno = last_tb.tb_lineno if last_tb else -1
        self.error_message = norm_msg

        if exc_type and exc_tb:
            self.traceback_str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        else:
            self.traceback_str = ""

        super().__init__(self.__str__())

    def __str__(self) -> str:
        base = f"Error in [{self.file_name}] at line [{self.lineno}] | Message: {self.error_message}"
        if self.traceback_str:
            return f"{base}\nTraceback:\n{self.traceback_str}"
        return base

    def to_dict(self) -> dict:
        return {
            "file": self.file_name,
            "line": self.lineno,
            "message": self.error_message,
            "traceback": self.traceback_str,
        }
