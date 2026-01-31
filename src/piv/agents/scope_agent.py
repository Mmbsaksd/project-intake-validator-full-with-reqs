
from ..agents.base import ValidationResult, ValidationIssue

def validate_scope(section):
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
    return ValidationResult(passed=len(issues)==0, issues=issues)
