import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

FEATURES = ["region", "age", "gender", "education_years", "income", "employed", "digital_access", "social_protection", "preferred_sector"]

def target_from_demo_data(df: pd.DataFrame) -> pd.Series:
    """Synthetic label definition; production must use observed longitudinal outcomes."""
    risk = (1-df.employed) * .40 + (df.income < df.income.median()) * .20 + (df.education_years < 12) * .15 + (1-df.digital_access) * .10 + (1-df.social_protection) * .10
    risk += df.preferred_sector.isin(["Administrative", "Retail"]) * .15
    return (risk >= .45).astype(int)

def train_risk_model(df: pd.DataFrame, seed: int = 42):
    x, y = df[FEATURES].copy(), target_from_demo_data(df)
    categorical = ["region", "gender", "preferred_sector"]
    numeric = [c for c in FEATURES if c not in categorical]
    prep = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), categorical), ("num", "passthrough", numeric)])
    model = Pipeline([("prep", prep), ("model", RandomForestClassifier(n_estimators=200, max_depth=6, class_weight="balanced", random_state=seed))])
    xtr, xte, ytr, yte = train_test_split(x, y, test_size=.25, random_state=seed, stratify=y)
    model.fit(xtr, ytr)
    p = model.predict_proba(xte)[:, 1]
    metrics = {"accuracy": accuracy_score(yte, p >= .5), "roc_auc": roc_auc_score(yte, p) if yte.nunique() > 1 else np.nan, "test_rows": len(yte)}
    scored = df.copy()
    scored["displacement_risk"] = model.predict_proba(x)[:, 1]
    scored["risk_band"] = pd.cut(scored.displacement_risk, [-.01, .35, .65, 1.01], labels=["Low", "Medium", "High"])
    return model, scored, metrics

def fairness_summary(scored: pd.DataFrame) -> pd.DataFrame:
    return scored.groupby("gender", as_index=False).agg(people=("person_id", "count"), average_risk=("displacement_risk", "mean"), high_risk_rate=("displacement_risk", lambda s: (s >= .65).mean()))

