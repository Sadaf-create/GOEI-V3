from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data"
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(42)
regions = pd.DataFrame({
    "region": ["North", "South", "East", "West", "Central", "Coastal"],
    "unemployment_rate": [.118,.151,.082,.105,.069,.132], "poverty_rate": [.185,.241,.121,.164,.097,.212],
    "median_income": [6200,5100,7900,6800,9200,5700], "skills_score": [61,52,73,66,81,57],
    "sme_density": [38,27,51,43,62,33], "digital_access": [72,61,84,78,91,67], "social_protection": [64,58,71,68,76,60]})
regions.to_csv(OUT/"regions.csv", index=False)
sectors = np.array(["Technology","Healthcare","Green Energy","Logistics","Retail","Administrative"])
skill_pool = {"Technology":["python","data analysis","digital literacy"],"Healthcare":["patient care","communication","digital literacy"],"Green Energy":["electrical","safety","data analysis"],"Logistics":["inventory","driving","digital literacy"],"Retail":["sales","customer service","digital literacy"],"Administrative":["office","communication","data entry"]}
rows=[]
for i in range(600):
    region=rng.choice(regions.region); sector=rng.choice(sectors); edu=int(rng.integers(6,21)); employed=int(rng.random() < (.58 + edu*.015))
    skills=rng.choice(skill_pool[sector], size=int(rng.integers(1,4)), replace=False)
    rows.append([f"P{i+1:04d}",region,int(rng.integers(18,61)),rng.choice(["Female","Male"]),edu,int(max(0,rng.normal(2500+edu*320+employed*1800,1500))),employed,int(rng.random()<.75),int(rng.random()<.65),"|".join(skills),sector])
pd.DataFrame(rows,columns=["person_id","region","age","gender","education_years","income","employed","digital_access","social_protection","skills","preferred_sector"]).to_csv(OUT/"people.csv",index=False)
titles = [("Junior Data Analyst","Technology","python|data analysis|digital literacy",.92,8500),("Cybersecurity Technician","Technology","networks|cybersecurity|digital literacy",.95,10000),("Care Coordinator","Healthcare","patient care|communication|digital literacy",.78,7000),("Solar Technician","Green Energy","electrical|safety|data analysis",.88,8200),("Supply Coordinator","Logistics","inventory|communication|digital literacy",.72,6800),("E-commerce Associate","Retail","sales|customer service|digital literacy",.66,6000),("Office Automation Assistant","Administrative","office|communication|data entry",.48,5500)]
jobs=[]
for i in range(70):
    title,sector,skills,growth,salary=titles[i%len(titles)]; jobs.append([f"J{i+1:03d}",title,sector,rng.choice(regions.region),skills,int(salary+rng.normal(0,500)),growth])
pd.DataFrame(jobs,columns=["job_id","title","sector","region","required_skills","salary","growth_score"]).to_csv(OUT/"jobs.csv",index=False)

