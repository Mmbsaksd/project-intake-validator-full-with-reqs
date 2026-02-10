
import sys
from pathlib import Path as PathlibPath
sys.path.insert(0, str(PathlibPath(__file__).parent.parent.parent.parent))

from pathlib import Path
from logger import CustomLogger
from exception import ValidationException

# Initialize logger
_logger_instance = CustomLogger()
logger = _logger_instance.get_logger(__name__)


def load_prompt(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError as e:
        logger.exception("Prompt file not found: %s", path)
        raise ValidationException(f"Prompt file not found: {path}", e) from e
    except Exception as e:
        logger.exception("Failed to load prompt: %s", path)
        raise ValidationException(f"Failed to load prompt: {path}", e) from e
