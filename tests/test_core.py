import pandas as pd
from src.opportunity import calculate_eoi
from src.matching import match_jobs
from src.simulation import simulate
from src.risk import train_risk_model

def test_eoi_range():
    x=pd.DataFrame({"region":["A","B"],"unemployment_rate":[.1,.2],"poverty_rate":[.1,.2],"median_income":[4,2],"skills_score":[8,4],"sme_density":[7,3],"digital_access":[9,5],"social_protection":[8,4]})
    assert calculate_eoi(x).opportunity_index.between(0,100).all()

def test_match_prefers_skill_overlap():
    p=pd.Series({"skills":"python|data analysis","preferred_sector":"Technology","region":"A"})
    j=pd.DataFrame([["1","Analyst","Technology","A","python|data analysis",10,.8],["2","Driver","Logistics","A","driving",10,.8]],columns=["job_id","title","sector","region","required_skills","salary","growth_score"])
    assert match_jobs(p,j).iloc[0].title == "Analyst"

def test_policy_reduces_rates():
    r=pd.DataFrame({"region":["A"],"unemployment_rate":[.2],"poverty_rate":[.3]})
    s=simulate(r,1,1,1,1).iloc[0]
    assert s.projected_unemployment_rate < .2 and s.projected_poverty_rate < .3

def test_risk_outputs_probability(tmp_path):
    rows=[]
    for i in range(80):
        bad=i%2
        rows.append([str(i),"A",25,"Female" if i%3 else "Male",8 if bad else 16,1000 if bad else 8000,0 if bad else 1,0 if bad else 1,0 if bad else 1,"office","Administrative" if bad else "Technology"])
    d=pd.DataFrame(rows,columns=["person_id","region","age","gender","education_years","income","employed","digital_access","social_protection","skills","preferred_sector"])
    _, scored, metrics=train_risk_model(d)
    assert scored.displacement_risk.between(0,1).all() and metrics["accuracy"] >= .8

