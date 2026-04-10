import pandas as pd
from readers.column_detector import detect_columns, apply_column_map

def read_excel(file) -> tuple:
    """Returns (df, mapping) where df has 'source'/'target' columns."""
    df = pd.read_excel(file, dtype=str).fillna("")
    df.columns = [str(c).strip() for c in df.columns]
    mapping = detect_columns(df)
    df = apply_column_map(df, mapping)
    return df, mapping
