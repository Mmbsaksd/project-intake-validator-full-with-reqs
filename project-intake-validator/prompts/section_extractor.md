
Extract and structure the document content into JSON using the exact ADSP template below.

Return ONLY valid JSON following this exact schema. All keys must be present; if a value is not available, return an empty string.

{
  "header": {
    "fields": {
      "Practice/Account": "",
      "Project Name": "",
      "Ticket Hyperlink": "",
      "Date": "",
      "Deadline": ""
    }
  },

  "business_case": {
    "fields": {
      "Why now": "",
      "Consequences of delay": "",
      "Technical justification": "",
      "Organizational KPI": ""
    }
  },

  "problem_statement": {
    "fields": {
      "Problem Definition": "",
      "Current Pain Points": "",
      "Business/System Impact": "",
      "Who is affected": ""
    }
  },

  "project_scope": {
    "fields": {
      "In Scope": "",
      "Out of Scope": ""
    }
  },

  "expected_benefits": {
    "fields": {
      "Qualitative Benefits": "",
      "Quantitative": {
        "Tech Hardware": "",
        "Custom Hardware": "",
        "Software": "",
        "Custom Software": ""
      }
    }
  }
}

DOCUMENT TO EXTRACT:
{DOCUMENT_TEXT}
