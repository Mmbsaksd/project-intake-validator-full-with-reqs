import openpyxl

def read_workbook_text(path: str) -> str:
    wb = openpyxl.load_workbook(path, data_only=True)
    parts = []
    for sheet in wb.worksheets:
        for row in sheet.iter_rows():
            row_vals = []
            for cell in row:
                val = str(cell.value).strip() if cell.value is not None else ""
                if val and cell.hyperlink:
                    target = cell.hyperlink.target
                    if target and target != val:
                        val = f"{val} ({target})"
                if val:
                    row_vals.append(val)
            if row_vals:
                parts.append(" ".join(row_vals))
    return "\n".join(parts)
