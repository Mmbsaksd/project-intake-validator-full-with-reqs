
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from logger import CustomLogger
from exception import ValidationException
from ..agents.base import ValidationResult, ValidationIssue

# Initialize logger
_logger_instance = CustomLogger()
logger = _logger_instance.get_logger(__name__)


def validate_scope(section):
    try:
        # Defensive: handle if section is string or not a dict
        if not isinstance(section, dict):
            section = {}
        f = section.get("fields", {})
        if not isinstance(f, dict):
            f = {}
        issues = []
        if not (f.get("In Scope") or "").strip():
            issues.append(ValidationIssue(field="In Scope", severity="ERROR", description="Missing"))
        if not (f.get("Out of Scope") or "").strip():
            issues.append(ValidationIssue(field="Out of Scope", severity="ERROR", description="Missing"))
        return ValidationResult(passed=len(issues) == 0, issues=issues)
    except Exception as e:
        logger.exception("Unhandled exception in validate_scope")
        raise ValidationException("validate_scope failed", e) from e
