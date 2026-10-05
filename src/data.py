from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

REQUIRED = {
    "regions": {"region", "unemployment_rate", "poverty_rate", "median_income", "skills_score", "sme_density", "digital_access", "social_protection"},
    "people": {"person_id", "region", "age", "gender", "education_years", "income", "employed", "digital_access", "social_protection", "skills", "preferred_sector"},
    "jobs": {"job_id", "title", "sector", "region", "required_skills", "salary", "growth_score"},
}

def validate(df: pd.DataFrame, kind: str) -> pd.DataFrame:
    missing = REQUIRED[kind] - set(df.columns)
    if missing:
        raise ValueError(f"{kind} CSV is missing columns: {', '.join(sorted(missing))}")
    return df.copy()

def load_default():
    return (
        validate(pd.read_csv(DATA_DIR / "regions.csv"), "regions"),
        validate(pd.read_csv(DATA_DIR / "people.csv"), "people"),
        validate(pd.read_csv(DATA_DIR / "jobs.csv"), "jobs"),
    )

