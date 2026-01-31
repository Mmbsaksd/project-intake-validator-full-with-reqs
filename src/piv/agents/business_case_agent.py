
from ..agents.base import ValidationResult, ValidationIssue

KEYWORDS_TECH = [
    "architecture", "latency", "throughput", "database", "integration", "API", "automation", "pipeline",
    "scalab", "scaling", "performance", "reliability", "availability"
]

KEYWORDS_KPI = ["KPI", "throughput", "uptime", "availability", "MTTR", "revenue", "cost", "productivity"]


def _is_weak(text: str, min_len: int = 30):
    return not text or len(text.strip()) < min_len


def _contains_keyword(text: str, keywords):
    if not text:
        return False
    t = text.lower()
    for k in keywords:
        if k.lower() in t:
            return True
    return False


def validate_business_case(section):
    # Defensive: handle if section is string or not a dict
    if not isinstance(section, dict):
        section = {}
    f = section.get("fields", {}) or {}
    issues = []

    why = (f.get("Why now") or "").strip()
    if not why:
        issues.append(ValidationIssue(field="Why now", severity="ERROR", description="Missing 'Why now'"))
    elif _is_weak(why):
        issues.append(ValidationIssue(field="Why now", severity="WARNING", description="Answer is weak or too short"))

    cons = (f.get("Consequences of delay") or "").strip()
    if not cons:
        issues.append(ValidationIssue(field="Consequences of delay", severity="ERROR", description="Missing consequences of delay"))
    elif _is_weak(cons):
        issues.append(ValidationIssue(field="Consequences of delay", severity="WARNING", description="Consequences description is weak or generic"))

    tech = (f.get("Technical justification") or "").strip()
    if not tech:
        issues.append(ValidationIssue(field="Technical justification", severity="ERROR", description="Missing technical justification"))
    else:
        if not _contains_keyword(tech, KEYWORDS_TECH):
            issues.append(ValidationIssue(field="Technical justification", severity="WARNING", description="Technical justification lacks technical details"))

    bigy = (f.get("Softtek Big Y") or "").strip()
    if not bigy:
        issues.append(ValidationIssue(field="Softtek Big Y", severity="ERROR", description="Missing Softtek Big Y"))

    kpi = (f.get("Organizational KPI") or "").strip()
    if not kpi:
        issues.append(ValidationIssue(field="Organizational KPI", severity="ERROR", description="Missing KPI alignment"))
    else:
        if not _contains_keyword(kpi, KEYWORDS_KPI):
            issues.append(ValidationIssue(field="Organizational KPI", severity="WARNING", description="KPI alignment not specific or missing KPI keywords"))

    return ValidationResult(passed=len([i for i in issues if i.severity == "ERROR"]) == 0, issues=issues)
