import pandas as pd
from lxml import etree

def read_tmx(file) -> tuple:
    try:
        tree = etree.parse(file)
        root = tree.getroot()
        rows = []
        for tu in root.findall(".//tu"):
            tuvs = tu.findall("tuv")
            src, tgt = "", ""
            for i, tuv in enumerate(tuvs):
                seg = tuv.find("seg")
                text = (seg.text or "") if seg is not None else ""
                if i == 0:
                    src = text
                else:
                    tgt = text
            rows.append({"source": src, "target": tgt})

        df = pd.DataFrame(rows).fillna("")
        mapping = {"source_col": "source", "target_col": "target",
                   "source_lang": "English", "target_lang": "Thai",
                   "extra_cols": [], "method": "TMX structure", "all_scores": {}}
        return df, mapping
    except Exception:
        return None, {}
