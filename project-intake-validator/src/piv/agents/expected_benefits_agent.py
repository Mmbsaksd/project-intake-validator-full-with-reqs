from ..agents.base import ValidationResult, ValidationIssue


def validate_expected_benefits(section):
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

    for k in ["Tech Hardware", "Custom Hardware", "Software", "Custom Software"]:
        v = (quant.get(k) or "") if quant else ""
        if not v or not str(v).strip():
            issues.append(ValidationIssue(field=f"Quantitative:{k}", severity="ERROR", description=f"Missing {k}"))

    return ValidationResult(passed=len([i for i in issues if i.severity == "ERROR"]) == 0, issues=issues)
