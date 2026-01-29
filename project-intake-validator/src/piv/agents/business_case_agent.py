
from ..agents.base import ValidationResult, ValidationIssue

def validate_business_case(section):
    # Defensive: handle if section is string or not a dict
    if not isinstance(section, dict):
        section = {}
    f = section.get("fields", {})
    if not isinstance(f, dict):
        f = {}
    issues = []
    if not (f.get("Problem Statement") or "").strip():
        issues.append(ValidationIssue(field="Problem Statement", severity="ERROR", description="Missing"))
    if not (f.get("Expected Benefits") or "").strip():
        issues.append(ValidationIssue(field="Expected Benefits", severity="ERROR", description="Missing"))
    if not (f.get("Key Metric") or "").strip():
        issues.append(ValidationIssue(field="Key Metric", severity="ERROR", description="Missing metric"))
    return ValidationResult(passed=len(issues)==0, issues=issues)
