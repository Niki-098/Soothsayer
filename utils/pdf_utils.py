import io
import pdfplumber
import pandas as pd

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    text_pages = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for p in pdf.pages:
            try:
                text = p.extract_text()
            except Exception:
                text = None
            if text:
                text_pages.append(text)
    return "\n\n".join(text_pages)

def extract_tables_from_pdf_bytes(pdf_bytes: bytes):
    dfs = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for p in pdf.pages:
            try:
                tables = p.extract_tables()
            except Exception:
                tables = []
            for table in tables:
                if not table:
                    continue
                df = pd.DataFrame(table)
                if df.shape[1] > 1:
                    df.columns = df.iloc[0]
                    df = df[1:].reset_index(drop=True)
                dfs.append(df)
    return dfs
