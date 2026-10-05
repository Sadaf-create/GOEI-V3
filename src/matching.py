import pandas as pd

def skills_set(value) -> set[str]:
    return {x.strip().lower() for x in str(value).split("|") if x.strip()}

def match_jobs(person: pd.Series, jobs: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    owned = skills_set(person["skills"])
    rows = []
    for _, job in jobs.iterrows():
        required = skills_set(job.required_skills)
        overlap = len(owned & required) / max(1, len(required))
        sector = 1.0 if str(person.preferred_sector).lower() == str(job.sector).lower() else 0.0
        region = 1.0 if person.region == job.region else .5
        score = 100 * (.60 * overlap + .25 * float(job.growth_score) + .10 * sector + .05 * region)
        missing = sorted(required - owned)
        rows.append({"job_id": job.job_id, "title": job.title, "sector": job.sector, "region": job.region, "salary": job.salary, "match_score": round(score, 1), "missing_skills": ", ".join(missing) or "None"})
    return pd.DataFrame(rows).sort_values("match_score", ascending=False).head(top_n)

