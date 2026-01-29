
import pandas as pd

def read_workbook_text(path: str) -> str:
    xls = pd.read_excel(path, sheet_name=None, header=None, dtype=str, engine="openpyxl")
    parts = []
    for _, df in xls.items():
        df = df.fillna("")
        for _, row in df.iterrows():
            vals = [v.strip() for v in row.tolist() if v and str(v).strip()]
            if vals:
                parts.append(" ".join(vals))
    return "\n".join(parts)
