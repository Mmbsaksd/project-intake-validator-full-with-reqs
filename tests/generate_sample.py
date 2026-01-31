import openpyxl
from pathlib import Path

def create_sample_excel(output_path):
    # Mock data that partially passes/fails validation
    # Header requires: Practice/Account, Project Name, Ticket Hyperlink (URL), Date, Deadline
    # Business Case requires: Why now, Consequences of delay, Technical justification, KPI alignment
    # Problem Statement requires: Problem Definition, Current Pain Points, Business/System Impact, Who is affected
    # Scope: In Scope, Out of Scope
    # Benefits: Qualitative, Quantitative (Tech HW, Custom HW, SW, Custom SW)
    
    data = [
        ["Section", "Field", "Value"],
        ["HEADER", "Practice/Account", "Digital Transformation / AI Lab"],
        ["HEADER", "Project Name", "Intake Validator Pilot"],
        ["HEADER", "Ticket Hyperlink", "BP-00479"],
        ["HEADER", "Date", "2026-01-31"],
        ["HEADER", "Deadline", "2026-03-15"],
        
        ["BUSINESS_CASE", "Why now", "The current manual process is slow and error-prone."],
        ["BUSINESS_CASE", "Consequences of delay", "Increased turnaround time and potential data entry errors."],
        ["BUSINESS_CASE", "Technical justification", "Leveraging LLMs for semantic validation of unstructured text."],
        ["BUSINESS_CASE", "Softtek Big Y", "Reduction in operational overhead."],
        ["BUSINESS_CASE", "Organizational KPI", "Efficiency improvement by 40%"],
        
        ["PROBLEM_STATEMENT", "Problem Definition", "Project intake documents are often incomplete or inconsistent."],
        ["PROBLEM_STATEMENT", "Current Pain Points", "Reviewers spend hours manually checking for mandatory information."],
        ["PROBLEM_STATEMENT", "Business/System Impact", "Delays in project kickoff and resource allocation."],
        ["PROBLEM_STATEMENT", "Who is affected", "Project Management Office (PMO) and Delivery Teams."],
        
        ["PROJECT_SCOPE", "In Scope", "Azure OpenAI integration, PDF/Excel support, LangGraph orchestration."],
        ["PROJECT_SCOPE", "Out of Scope", "Legacy system migration, SAP integration."],
        
        ["EXPECTED_BENEFITS", "Qualitative Benefits", "Improved data quality and faster approval cycles."],
        ["EXPECTED_BENEFITS", "Softtek Hard Dollars", "$50,000"],
        ["EXPECTED_BENEFITS", "Softtek Soft Dollars", "$10,000"],
        ["EXPECTED_BENEFITS", "Customer Hard Dollars", "$100,000"],
        ["EXPECTED_BENEFITS", "Customer Soft Dollars", "$20,000"]
    ]
    
    # Create workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    
    for r_idx, row in enumerate(data, 1):
        for c_idx, val in enumerate(row, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            # Add hyperlink to the Ticket Hyperlink value (row 4, col 3 assuming column 1 is Section, 2 is Field, 3 is Value)
            if r_idx == 4 and c_idx == 3:
                cell.hyperlink = "https://jira.example.com/browse/BP-00479"
                cell.font = openpyxl.styles.Font(color="0000FF", underline="single")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    print(f"Created sample Excel with hyperlinks at: {output_path}")

if __name__ == "__main__":
    import sys
    create_sample_excel(sys.argv[1])
