from ..agents.base import ValidationResult, ValidationIssue


def validate_problem(section):
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
