
from pydantic import BaseModel
from typing import List

class ValidationIssue(BaseModel):
    field: str
    severity: str
    description: str

class ValidationResult(BaseModel):
    passed: bool
    issues: List[ValidationIssue] = []
