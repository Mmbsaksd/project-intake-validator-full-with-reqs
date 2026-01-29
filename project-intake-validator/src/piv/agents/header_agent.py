
from ..agents.base import ValidationResult, ValidationIssue

def validate_header(section):
    # Defensive: handle if section is string or not a dict
    if not isinstance(section, dict):
        section = {}
    f = section.get("fields", {})
    if not isinstance(f, dict):
        f = {}
    issues = []
    if not (f.get("Project Name") or "").strip():
        issues.append(ValidationIssue(field="Project Name", severity="ERROR", description="Project name missing"))
    return ValidationResult(passed=len(issues)==0, issues=issues)
