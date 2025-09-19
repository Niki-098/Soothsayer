import io
import pandas as pd

def extract_from_excel_bytes(excel_bytes: bytes):
    """
    Extract all sheets from Excel bytes and return as a dict of DataFrames.
    Tries openpyxl engine first, falls back to default if needed.
    """
    excel_io = io.BytesIO(excel_bytes)
    try:
        sheets = pd.read_excel(excel_io, sheet_name=None, engine="openpyxl")
    except Exception:
        excel_io.seek(0)
        sheets = pd.read_excel(excel_io, sheet_name=None)
    # Ensure all values are DataFrames
    sheets = {k: v if isinstance(v, pd.DataFrame) else pd.DataFrame(v) for k, v in sheets.items()}
    return sheets
