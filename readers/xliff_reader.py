import pandas as pd
from lxml import etree

def read_xliff(file) -> tuple:
    try:
        tree = etree.parse(file)
        root = tree.getroot()
        ns = {"x": "urn:oasis:names:tc:xliff:document:1.2"}
        rows = []

        for unit in root.findall(".//x:trans-unit", ns):
            src = unit.find("x:source", ns)
            tgt = unit.find("x:target", ns)
            rows.append({
                "source": (src.text or "") if src is not None else "",
                "target": (tgt.text or "") if tgt is not None else "",
            })

        if not rows:
            ns20 = "urn:oasis:names:tc:xliff:document:2.0"
            for unit in root.findall(f".//{{{ns20}}}unit"):
                src = unit.find(f".//{{{ns20}}}source")
                tgt = unit.find(f".//{{{ns20}}}target")
                rows.append({
                    "source": (src.text or "") if src is not None else "",
                    "target": (tgt.text or "") if tgt is not None else "",
                })

        df = pd.DataFrame(rows).fillna("")
        mapping = {"source_col": "source", "target_col": "target",
                   "source_lang": "English", "target_lang": "Thai",
                   "extra_cols": [], "method": "XLIFF structure", "all_scores": {}}
        return df, mapping
    except Exception as e:
        return None, {}
