
def format_feedback(validation):
    if all(v.passed for v in validation.values()):
        return "All good. You can go ahead."
    lines = ["Feedback"]
    for sec, res in validation.items():
        for i in res.issues:
            lines.append(f"- [{sec}] {i.field}: {i.description}")
    return "\n".join(lines)
