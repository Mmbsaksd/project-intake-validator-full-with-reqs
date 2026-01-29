
def format_feedback(validation):
    """Produce a strict ADSP Validation Summary matching the user's required format.

    `validation` is a dict mapping section keys to ValidationResult objects.
    """
    # Helper to convert result
    def sec_passed(section_key):
        res = validation.get(section_key)
        if res is None:
            return False
        return bool(res.passed)

    # HEADER
    # For each header field, it's valid if there is no ERROR issue for that specific field
    hdr = validation.get("header")
    hdr_issues = hdr.issues if hdr else []
    def hdr_ok(field_name):
        return not any(i.field == field_name and i.severity == "ERROR" for i in hdr_issues)

    header_checks = {
        "Practice/Account": hdr_ok("Practice/Account"),
        "Project Name": hdr_ok("Project Name"),
        "Ticket Hyperlink": hdr_ok("Ticket Hyperlink"),
        "Date": hdr_ok("Date"),
        "Deadline": hdr_ok("Deadline"),
    }

    # BUSINESS CASE
    bc = validation.get("business_case")
    business_checks = {
        "Why now": False,
        "Consequences of delay": False,
        "Technical justification": False,
        "KPI alignment": False,
    }
    if bc:
        # mark as True unless there is an ERROR issue for that field
        for k in list(business_checks.keys()):
            if not any(i.field == k and i.severity == "ERROR" for i in bc.issues):
                business_checks[k] = True

    # PROBLEM STATEMENT
    prob = validation.get("problem_statement")
    problem_clarity = False
    problem_completeness = False
    if prob:
        # clarity: no ERROR for Problem Definition
        if not any(i.field == "Problem Definition" and i.severity == "ERROR" for i in prob.issues):
            problem_clarity = True
        # completeness: no ERROR for required fields
        required_problem_fields = ["Problem Definition", "Current Pain Points", "Business/System Impact", "Who is affected"]
        if not any(i.field in required_problem_fields and i.severity == "ERROR" for i in prob.issues):
            problem_completeness = True

    # PROJECT SCOPE
    scope = validation.get("project_scope")
    in_scope_ok = False
    out_scope_ok = False
    if scope:
        if not any(i.field == "In Scope" and i.severity == "ERROR" for i in scope.issues):
            in_scope_ok = True
        if not any(i.field == "Out of Scope" and i.severity == "ERROR" for i in scope.issues):
            out_scope_ok = True

    # EXPECTED BENEFITS
    eb = validation.get("expected_benefits")
    qual_ok = False
    quant_ok = {"Tech Hardware": False, "Custom Hardware": False, "Software": False, "Custom Software": False}
    if eb:
        if not any(i.field == "Qualitative Benefits" and i.severity == "ERROR" for i in eb.issues):
            qual_ok = True
        for k in quant_ok.keys():
            if not any(i.field == f"Quantitative:{k}" and i.severity == "ERROR" for i in eb.issues):
                quant_ok[k] = True

    # Build the exact output format
    lines = []
    lines.append("ADSP Validation Summary\n")
    lines.append("HEADER:")
    lines.append(f"Practice/Account: {'✅' if header_checks['Practice/Account'] else '❌'}")
    lines.append(f"Project Name: {'✅' if header_checks['Project Name'] else '❌'}")
    lines.append(f"Ticket Hyperlink: {'✅' if header_checks['Ticket Hyperlink'] else '❌'}")
    lines.append(f"Date: {'✅' if header_checks['Date'] else '❌'}")
    lines.append(f"Deadline: {'✅' if header_checks['Deadline'] else '❌'}\n")

    lines.append("BUSINESS CASE:")
    lines.append(f"Why now: {'✅' if business_checks['Why now'] else '❌'}")
    lines.append(f"Consequences of delay: {'✅' if business_checks['Consequences of delay'] else '❌'}")
    lines.append(f"Technical justification: {'✅' if business_checks['Technical justification'] else '❌'}")
    lines.append(f"KPI alignment: {'✅' if business_checks['KPI alignment'] else '❌'}\n")

    lines.append("PROBLEM STATEMENT:")
    lines.append(f"Clarity: {'✅' if problem_clarity else '❌'}")
    lines.append(f"Completeness: {'✅' if problem_completeness else '❌'}\n")

    lines.append("PROJECT SCOPE:")
    lines.append(f"In Scope: {'✅' if in_scope_ok else '❌'}")
    lines.append(f"Out of Scope: {'✅' if out_scope_ok else '❌'}\n")

    lines.append("EXPECTED BENEFITS:")
    lines.append(f"Qualitative benefits: {'✅' if qual_ok else '❌'}")
    lines.append("Quantitative benefits:")
    lines.append(f"Tech Hardware: {'✅' if quant_ok['Tech Hardware'] else '❌'}")
    lines.append(f"Custom Hardware: {'✅' if quant_ok['Custom Hardware'] else '❌'}")
    lines.append(f"Software: {'✅' if quant_ok['Software'] else '❌'}")
    lines.append(f"Custom Software: {'✅' if quant_ok['Custom Software'] else '❌'}\n")

    overall_ok = all([
        header_checks['Practice/Account'], header_checks['Project Name'], header_checks['Ticket Hyperlink'], header_checks['Date'], header_checks['Deadline'],
        business_checks['Why now'], business_checks['Consequences of delay'], business_checks['Technical justification'], business_checks['KPI alignment'],
        problem_clarity, problem_completeness, in_scope_ok, out_scope_ok, qual_ok, all(quant_ok.values())
    ])

    lines.append("OVERALL STATUS:\n")
    lines.append("READY FOR REVIEW" if overall_ok else "NEEDS REVISION")

    return "\n".join(lines)
