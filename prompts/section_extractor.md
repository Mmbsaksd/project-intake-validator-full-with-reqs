Extract and structure the document content into JSON using the exact ADSP template below.

QUALITY INSTRUCTIONS:
1. **Field Alignment**: Use the "Start Date" field for the project commencement date.
2. **Project Name Fallback**: If the specific cell for "Project Name" is empty or contains placeholders like "[Project Name]", look at the top of the document (the main title, usually above "Action Plan") and use that as the Project Name.
3. **Date Precision**: Distinguish clearly between "Start Date" and "Deadline". "Start Date" is when the project begins; "Deadline" is the target completion date. Capture them exactly as written in the document.
4. **Ticket Hyperlink**: If a ticket ID (e.g., BP-00479) is followed by a URL in parentheses, capture the entire string: "ID (URL)".
5. **Quantitative Benefits**: Look specifically for "Softtek Hard Dollars", "Softtek Soft Dollars", "Customer Hard Dollars", and "Customer Soft Dollars". These are typically numeric values or currency.

Return ONLY valid JSON following this exact schema. All keys must be present; if a value is not available, return an empty string.

{
  "header": {
    "fields": {
      "Practice/Account": "",
      "Project Name": "",
      "Ticket Hyperlink": "",
      "Start Date": "",
      "Deadline": ""
    }
  },

  "business_case": {
    "fields": {
      "Why now": "",
      "Consequences of delay": "",
      "Technical justification": "",
      "Softtek Big Y": "",
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
        "Softtek Hard Dollars": "",
        "Softtek Soft Dollars": "",
        "Customer Hard Dollars": "",
        "Customer Soft Dollars": ""
      }
    }
  }
}

DOCUMENT TO EXTRACT:
{DOCUMENT_TEXT}
