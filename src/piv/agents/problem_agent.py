import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from logger import CustomLogger
from exception import ValidationException
from ..agents.base import ValidationResult, ValidationIssue

# Initialize logger
_logger_instance = CustomLogger()
logger = _logger_instance.get_logger(__name__)


def validate_problem(section):
    try:
        if not isinstance(section, dict):
            section = {}
        f = section.get("fields", {}) or {}
        issues = []

        pd = (f.get("Problem Definition") or "").strip()
        if not pd:
            issues.append(ValidationIssue(field="Problem Definition", severity="ERROR", description="Missing problem definition"))
        elif len(pd) < 30:
            issues.append(ValidationIssue(field="Problem Definition", severity="WARNING", description="Problem definition is short or vague"))

        pain = (f.get("Current Pain Points") or "").strip()
        if not pain:
            issues.append(ValidationIssue(field="Current Pain Points", severity="ERROR", description="Missing current pain points"))

        impact = (f.get("Business/System Impact") or "").strip()
        if not impact:
            issues.append(ValidationIssue(field="Business/System Impact", severity="ERROR", description="Missing business/system impact"))

        who = (f.get("Who is affected") or "").strip()
        if not who:
            issues.append(ValidationIssue(field="Who is affected", severity="ERROR", description="Missing affected stakeholders or teams"))

        return ValidationResult(passed=len([i for i in issues if i.severity == "ERROR"]) == 0, issues=issues)
    except Exception as e:
        logger.exception("Unhandled exception in validate_problem")
        raise ValidationException("validate_problem failed", e) from e
