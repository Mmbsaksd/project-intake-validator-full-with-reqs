import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from logger import CustomLogger
from exception import ValidationException
from ..agents.base import ValidationResult, ValidationIssue

# Initialize logger
_logger_instance = CustomLogger()
logger = _logger_instance.get_logger(__name__)


def validate_expected_benefits(section):
    try:
        if not isinstance(section, dict):
            section = {}
        f = section.get("fields", {}) or {}
        issues = []

        qual = (f.get("Qualitative Benefits") or "").strip()
        if not qual:
            issues.append(ValidationIssue(field="Qualitative Benefits", severity="ERROR", description="Missing qualitative benefits"))
        elif len(qual) < 20:
            issues.append(ValidationIssue(field="Qualitative Benefits", severity="WARNING", description="Qualitative benefits vague or short"))

        quant = f.get("Quantitative") or {}
        if not isinstance(quant, dict):
            quant = {}

        for k in ["Softtek Hard Dollars", "Softtek Soft Dollars", "Customer Hard Dollars", "Customer Soft Dollars"]:
            v = (quant.get(k) or "") if quant else ""
            if not v or not str(v).strip():
                issues.append(ValidationIssue(field=f"Quantitative:{k}", severity="ERROR", description=f"Missing {k}"))

        return ValidationResult(passed=len([i for i in issues if i.severity == "ERROR"]) == 0, issues=issues)
    except Exception as e:
        logger.exception("Unhandled exception in validate_expected_benefits")
        raise ValidationException("validate_expected_benefits failed", e) from e
