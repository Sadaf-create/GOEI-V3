import numpy as np
import pandas as pd

DEFAULT_WEIGHTS = {"employment": .25, "income": .20, "skills": .20, "enterprise": .15, "digital": .10, "protection": .10}

def minmax(s: pd.Series, reverse: bool = False) -> pd.Series:
    s = pd.to_numeric(s, errors="coerce").fillna(s.median())
    span = s.max() - s.min()
    out = pd.Series(0.5, index=s.index) if span == 0 else (s - s.min()) / span
    return 1 - out if reverse else out

def calculate_eoi(regions: pd.DataFrame, weights=None) -> pd.DataFrame:
    w = weights or DEFAULT_WEIGHTS
    x = regions.copy()
    components = {
        "employment": minmax(x.unemployment_rate, True),
        "income": minmax(x.median_income),
        "skills": minmax(x.skills_score),
        "enterprise": minmax(x.sme_density),
        "digital": minmax(x.digital_access),
        "protection": minmax(x.social_protection),
    }
    x["opportunity_index"] = sum(components[k] * w[k] for k in w) * 100
    x["deprivation_score"] = 100 - x.opportunity_index
    x["priority"] = pd.cut(x.deprivation_score, [-1, 40, 65, 101], labels=["Low", "Medium", "High"])
    return x.sort_values("opportunity_index", ascending=False).reset_index(drop=True)

