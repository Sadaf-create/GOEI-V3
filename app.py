import io
import pandas as pd
import plotly.express as px
import streamlit as st
from src.data import load_default, validate
from src.opportunity import calculate_eoi
from src.risk import train_risk_model, fairness_summary
from src.matching import match_jobs
from src.simulation import simulate

st.set_page_config(page_title="GOIP", page_icon="🌍", layout="wide")
st.title("Global Opportunity Intelligence Platform")
st.caption("GOEI decision-support prototype · synthetic demonstration data")

if "data" not in st.session_state:
    st.session_state.data = load_default()
regions, people, jobs = st.session_state.data

page=st.sidebar.radio("Module",["Executive dashboard","Opportunity index","Early warning","Skills-to-jobs","Policy simulator","Data & methodology"])

def download(df,name):
    st.download_button("Download results (CSV)",df.to_csv(index=False).encode(),name,"text/csv")

if page=="Executive dashboard":
    eoi=calculate_eoi(regions); _,scored,metrics=train_risk_model(people)
    a,b,c,d=st.columns(4)
    a.metric("People represented",f"{len(people):,}"); b.metric("Vacancies",f"{len(jobs):,}"); c.metric("Mean opportunity",f"{eoi.opportunity_index.mean():.1f}/100"); d.metric("High-risk share",f"{(scored.displacement_risk>=.65).mean():.1%}")
    st.plotly_chart(px.bar(eoi,x="region",y="opportunity_index",color="priority",title="Economic Opportunity Index by region",range_y=[0,100]),use_container_width=True)
    st.info("Outputs prioritise human review. No individual eligibility or hiring decision is made.")

elif page=="Opportunity index":
    st.subheader("Transparent composite Economic Opportunity Index")
    st.write("Weights: employment 25%, income 20%, skills 20%, enterprise 15%, digital access 10%, social protection 10%.")
    eoi=calculate_eoi(regions)
    st.plotly_chart(px.scatter(eoi,x="opportunity_index",y="poverty_rate",size="sme_density",color="priority",hover_name="region",range_x=[0,100]),use_container_width=True)
    st.dataframe(eoi,use_container_width=True,hide_index=True); download(eoi,"goip_opportunity_index.csv")

elif page=="Early warning":
    st.subheader("Labour-displacement early warning")
    _,scored,metrics=train_risk_model(people)
    a,b,c=st.columns(3); a.metric("Test accuracy",f"{metrics['accuracy']:.1%}"); b.metric("Test ROC-AUC",f"{metrics['roc_auc']:.2f}"); c.metric("High-risk records",int((scored.displacement_risk>=.65).sum()))
    by_region=scored.groupby("region",as_index=False).agg(average_risk=("displacement_risk","mean"),people=("person_id","count"))
    st.plotly_chart(px.bar(by_region,x="region",y="average_risk",color="average_risk",range_y=[0,1]),use_container_width=True)
    st.markdown("**Fairness monitoring (audit only)**"); st.dataframe(fairness_summary(scored),hide_index=True,use_container_width=True)
    st.warning("The target labels are generated for demonstration. A production model requires observed longitudinal outcomes, representative validation, explainability and independent audit.")
    download(scored[["person_id","region","displacement_risk","risk_band"]],"goip_early_warning.csv")

elif page=="Skills-to-jobs":
    st.subheader("Explainable skills-to-jobs matching")
    pid=st.selectbox("Select a synthetic beneficiary",people.person_id)
    person=people.loc[people.person_id==pid].iloc[0]
    st.write({"region":person.region,"current skills":person.skills,"preferred sector":person.preferred_sector})
    matches=match_jobs(person,jobs,10)
    st.dataframe(matches,use_container_width=True,hide_index=True); download(matches,"goip_job_matches.csv")

elif page=="Policy simulator":
    st.subheader("Illustrative policy scenario")
    st.caption("Values are coverage/intensity from 0 to 100%. Elasticities are transparent assumptions, not causal estimates.")
    a,b=st.columns(2)
    training=a.slider("Accredited training coverage",0.,1.,.35,.05); sme=b.slider("SME support intensity",0.,1.,.30,.05)
    digital=a.slider("Digital investment intensity",0.,1.,.25,.05); protection=b.slider("Social-protection expansion",0.,1.,.25,.05)
    sim=simulate(regions,training,sme,digital,protection)
    st.plotly_chart(px.bar(sim,x="region",y=["unemployment_rate","projected_unemployment_rate"],barmode="group",title="Baseline versus scenario unemployment"),use_container_width=True)
    st.dataframe(sim,use_container_width=True,hide_index=True); download(sim,"goip_policy_scenario.csv")

else:
    st.subheader("Data ingestion and methodology")
    st.write("Upload all three files to replace the sample data for this session. Required columns are checked before use.")
    ur=st.file_uploader("Regional indicators CSV",type="csv"); up=st.file_uploader("People CSV",type="csv"); uj=st.file_uploader("Vacancies CSV",type="csv")
    if st.button("Validate and load uploads"):
        if not all([ur,up,uj]): st.error("Please upload all three CSV files.")
        else:
            try:
                st.session_state.data=(validate(pd.read_csv(ur),"regions"),validate(pd.read_csv(up),"people"),validate(pd.read_csv(uj),"jobs")); st.success("Files validated and loaded."); st.rerun()
            except Exception as e: st.error(str(e))
    refs=pd.read_csv("data/reference_indicators.csv")
    st.markdown("**Verified reference indicators (context only)**"); st.dataframe(refs,use_container_width=True,hide_index=True)
    st.markdown("**Governance controls for production:** purpose limitation; minimisation; pseudonymous IDs; access logs; consent/legal basis; versioned data; confidence limits; bias audit; human review; appeal mechanism; independent impact evaluation.")
