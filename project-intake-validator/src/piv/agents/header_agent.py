
from ..agents.base import ValidationResult, ValidationIssue
from datetime import datetime


def _is_valid_date(s: str):
    if not s or not isinstance(s, str):
        return False
    s = s.strip()
    formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y"]
    for fmt in formats:
        try:
            datetime.strptime(s, fmt)
            return True
        except Exception:
            continue
    return False


def validate_header(section):
    # Defensive: handle if section is string or not a dict
    if not isinstance(section, dict):
        section = {}
    f = section.get("fields", {}) or {}
    issues = []

    if not (f.get("Practice/Account") or "").strip():
        issues.append(ValidationIssue(field="Practice/Account", severity="ERROR", description="Missing Practice/Account"))

    if not (f.get("Project Name") or "").strip():
        issues.append(ValidationIssue(field="Project Name", severity="ERROR", description="Missing Project Name"))

    ticket = (f.get("Ticket Hyperlink") or "").strip()
    if not ticket:
        issues.append(ValidationIssue(field="Ticket Hyperlink", severity="ERROR", description="Missing ticket hyperlink"))
    else:
        if not (ticket.startswith("http://") or ticket.startswith("https://")):
            issues.append(ValidationIssue(field="Ticket Hyperlink", severity="ERROR", description="Ticket hyperlink not a clickable URL"))

    date_val = (f.get("Date") or "").strip()
    if not date_val or not _is_valid_date(date_val):
        issues.append(ValidationIssue(field="Date", severity="ERROR", description="Missing or invalid date"))

    deadline = (f.get("Deadline") or "").strip()
    if not deadline or not _is_valid_date(deadline):
        issues.append(ValidationIssue(field="Deadline", severity="ERROR", description="Missing or invalid deadline"))

    return ValidationResult(passed=len(issues) == 0, issues=issues)
