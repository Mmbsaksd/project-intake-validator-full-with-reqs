import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import openpyxl
from logger import CustomLogger
from exception import ValidationException

# Initialize logger
_logger_instance = CustomLogger()
logger = _logger_instance.get_logger(__name__)


def read_workbook_text(path: str) -> str:
    """Read all non-empty cell text from workbook and return as plain text.

    This helper logs and wraps errors in ValidationException for callers.
    """
    try:
        wb = openpyxl.load_workbook(path, data_only=True)
        parts = []
        for sheet in wb.worksheets:
            for row in sheet.iter_rows():
                row_vals = []
                for cell in row:
                    val = str(cell.value).strip() if cell.value is not None else ""
                    if val and getattr(cell, "hyperlink", None):
                        target = cell.hyperlink.target
                        if target and target != val:
                            val = f"{val} ({target})"
                    if val:
                        row_vals.append(val)
                if row_vals:
                    parts.append(" ".join(row_vals))
        return "\n".join(parts)
    except FileNotFoundError as e:
        logger.exception("Excel file not found: %s", path)
        raise ValidationException(f"Excel file not found: {path}", e) from e
    except Exception as e:
        logger.exception("Failed to read workbook: %s", path)
        raise ValidationException(f"Failed to read workbook: {path}", e) from e
