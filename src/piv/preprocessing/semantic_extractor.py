
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from ..llm.prompts import load_prompt
from logger import CustomLogger
from exception import ValidationException

# Initialize logger
_logger_instance = CustomLogger()
logger = _logger_instance.get_logger(__name__)


def extract_sections_via_llm(text, prompts_dir, llm):
    try:
        prompt = load_prompt(f"{prompts_dir}/section_extractor.md")
        payload = prompt.replace("{DOCUMENT_TEXT}", text)
        return llm.complete_json("", payload)
    except Exception as e:
        logger.exception("Failed to extract sections via LLM")
        raise ValidationException("extract_sections_via_llm failed", e) from e
