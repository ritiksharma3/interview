"""Candidate Screening Dashboard demo. Run: pip install streamlit pandas plotly && streamlit run candidate_dashboard.py
All values are hard-coded examples. Replace with reviewed transcript/model outputs before production.
CV gaze/head signals are review cues, never proof of cheating or honesty."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Candidate Intelligence | Screening", page_icon="◈", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}.stApp{background:#f4f7fb}.block-container{padding-top:1.5rem;max-width:1500px}
h1,h2,h3{font-family:Manrope,sans-serif;color:#152238}.hero{background:linear-gradient(120deg,#101e35,#1c3558 62%,#345d78);border-radius:22px;padding:27px 30px;color:white;margin-bottom:18px;box-shadow:0 12px 32px #101e351f}.hero-kicker{color:#a9c8e9;text-transform:uppercase;letter-spacing:2px;font-size:11px;font-weight:700}.hero h1{color:white;font-size:31px;margin:6px 0}.hero p{color:#d3deeb;margin:0;font-size:14px}.section-note{color:#6b7b91;font-size:13px;margin-top:-8px;margin-bottom:14px}.insight{border-left:4px solid #6d91c6;background:#f7faff;padding:12px 14px;border-radius:0 11px 11px 0;margin-bottom:9px}.insight-title{font-weight:700;color:#1d3556;margin-bottom:3px}.insight-body{color:#52647c;font-size:13px}.footer{color:#7c899b;font-size:11px;text-align:center;padding:22px 0}
div[data-testid="stMetric"]{background:white;padding:13px 16px;border:1px solid #e5eaf1;border-radius:15px}div[data-testid="stMetricLabel"]{color:#64748b}div[data-testid="stMetricValue"]{color:#172a45}
</style>""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# DEMO DATA: all candidate details, ratings and events below are fictional.
# Connect these to your transcript/rubric/monitoring pipeline later.
# -------------------------------------------------------------------
candidate = {"name":"Aarav Mehta","candidate_id":"CND-2026-0148","role":"AI / Data Science Intern","stage":"Screening Round","interviewer":"Neha Kapoor","date":"12 Oct 2026","start_time":"10:02 AM","duration_min":34,"experience":"2.1 years","skills":["Python","SQL","Machine Learning","NLP","APIs"]}
scores = {"Concept clarity":82,"Confidence / delivery":76,"Communication clarity":85,"Problem-solving":79,"Role alignment":84,"Evidence-backed answers":72}
details = {
"Concept clarity":{"summary":"Explains core ideas accurately and usually connects them to examples.","evidence":["Explained train/validation/test split and why leakage matters.","Distinguished classification metrics and gave a practical use case."],"probe":"Ask a follow-up numerical question on precision/recall trade-offs."},
"Confidence / delivery":{"summary":"Generally structured delivery; paused on unfamiliar model-selection questions.","evidence":["Used a clear answer structure for familiar topics.","Asked for clarification once rather than guessing."],"probe":"Use an unfamiliar scenario to assess reasoning aloud. This score is delivery evidence, not a personality assessment."},
"Communication clarity":{"summary":"Answers were easy to follow and mostly concise, with occasional jargon.","evidence":["Summarised the approach before implementation details.","One answer needed a prompt to explain business impact in plain language."],"probe":"Ask for a 60-second explanation to a non-technical stakeholder."},
"Problem-solving":{"summary":"Shows sensible decomposition; validation strategy could be stronger.","evidence":["Separated data-quality checks from model evaluation.","Mentioned baseline comparison but did not consistently quantify trade-offs."],"probe":"Give a small case with missing data, a baseline and a latency constraint."},
"Role alignment":{"summary":"Relevant Python/SQL experience and interest in applied ML use cases.","evidence":["Connected prior API work to data-pipeline reliability.","Has practical exposure to NLP and model evaluation."],"probe":"Validate hands-on ownership and deployment experience."},
"Evidence-backed answers":{"summary":"Some examples included outcomes; metrics and personal contribution were not always explicit.","evidence":["Provided a concrete project example.","Could better separate personal contribution from team outcome."],"probe":"Ask for baseline, metric, time period and exact individual contribution."}}
pros=[("Strong fundamentals","Explains several core ML concepts accurately and connects them to practical examples."),("Clear communication","Usually gives structured answers and can summarise the main point."),("Relevant hands-on exposure","Examples span Python/SQL, APIs and applied NLP."),("Clarifies uncertainty","Asked for clarification on an unfamiliar prompt instead of inventing an answer.")]
cons=[("Evaluation depth to verify","Metric selection and validation trade-offs were not equally detailed in every answer."),("Impact metrics are inconsistent","Some project claims need a baseline, measurement period and attributable outcome."),("Deployment ownership is unclear","Probe monitoring, rollback, reproducibility and production responsibility.")]
followups=[{"Priority":"High","Topic":"Model evaluation","Question":"Given an imbalanced dataset, when would you optimise precision versus recall?","Why":"Tests conceptual depth and trade-off reasoning."},{"Priority":"High","Topic":"Project ownership","Question":"Which components did you personally build, and what measurable result changed?","Why":"Separates individual contribution from team output."},{"Priority":"Medium","Topic":"Production thinking","Question":"How would you monitor data drift and decide when to retrain?","Why":"Tests operational maturity."},{"Priority":"Medium","Topic":"Communication","Question":"Explain your last project to a non-technical product manager in one minute.","Why":"Checks audience adaptation."}]
questions=pd.DataFrame([{"Question":"Python / data","Score":88,"Evidence":"Strong example"},{"Question":"SQL","Score":84,"Evidence":"Correct approach"},{"Question":"ML fundamentals","Score":81,"Evidence":"Mostly correct"},{"Question":"Model evaluation","Score":70,"Evidence":"Needed a prompt"},{"Question":"Project ownership","Score":68,"Evidence":"Impact unclear"},{"Question":"Production design","Score":74,"Evidence":"Partial depth"}])
integrity={"photos":2040,"windows":68,"face_missing":2,"multiple_people":1,"gaze":7,"head":5,"devices":1}

with st.sidebar:
    st.markdown("## ◈ Candidate Intelligence")
    st.caption("SCREENING WORKSPACE")
    page=st.radio("Dashboard section",["Executive overview","Competency analysis","Pros & development areas","Integrity review","Interview evidence"])
    st.divider(); st.markdown("**Candidate**"); st.write(candidate["name"]); st.caption(candidate["candidate_id"])
    st.markdown("**Interview details**"); st.write(candidate["role"]); st.caption(f'{candidate["date"]} · {candidate["start_time"]}')
    st.divider(); st.warning("DEMO MODE — all values are hard-coded examples. Do not use them for a real hiring decision.")

st.markdown(f'<div class="hero"><div class="hero-kicker">Talent intelligence · Screening report</div><h1>{candidate["name"]}</h1><p>{candidate["role"]} &nbsp; · &nbsp; {candidate["stage"]} &nbsp; · &nbsp; {candidate["candidate_id"]}</p></div>',unsafe_allow_html=True)
k1,k2,k3,k4,k5=st.columns(5)
k1.metric("Interview duration",f'{candidate["duration_min"]} min',"Recorded session")
k2.metric("Concept clarity",f'{scores["Concept clarity"]}/100',"Rubric score")
k3.metric("Communication",f'{scores["Communication clarity"]}/100',"Rubric score")
k4.metric("Problem-solving",f'{scores["Problem-solving"]}/100',"Rubric score")
k5.metric("Review windows",str(integrity["windows"]),"CV review queue")
st.caption("Scores are illustrative rubric ratings from interview evidence—not objective measurements of character or future performance.")

def heading(title, subtitle=None):
    st.subheader(title)
    if subtitle: st.markdown(f'<div class="section-note">{subtitle}</div>',unsafe_allow_html=True)
def insight(title, body, color="#6d91c6"):
    st.markdown(f'<div class="insight" style="border-left-color:{color}"><div class="insight-title">{title}</div><div class="insight-body">{body}</div></div>',unsafe_allow_html=True)

if page=="Executive overview":
    left,right=st.columns([1.15,1])
    with left:
        heading("Candidate snapshot","A concise, evidence-oriented view for the hiring panel.")
        st.markdown('<div class="insight"><div class="insight-title">Role alignment · promising, validate depth</div><div class="insight-body">Relevant Python/SQL and applied ML exposure. Follow up on evaluation trade-offs, personal project ownership and production readiness.</div></div>',unsafe_allow_html=True)
        a,b,c=st.columns(3); a.metric("Experience",candidate["experience"]); b.metric("Competencies",len(scores)); c.metric("Follow-up probes",len(followups))
        st.markdown("**Reported skill areas**  "); st.write(" · ".join(candidate["skills"]))
        heading("Interview signal timeline","Illustrative five-minute intervals; replace with transcript timestamps.")
        timeline=pd.DataFrame({"Time":["00–05","05–10","10–15","15–20","20–25","25–30","30–34"],"Clarity":[78,82,86,73,80,87,84],"Technical depth":[70,77,85,68,76,82,78]})
        fig=px.line(timeline,x="Time",y=["Clarity","Technical depth"],markers=True,color_discrete_sequence=["#3166a8","#21a179"]); fig.update_layout(height=300,margin=dict(l=8,r=8,t=15,b=5),paper_bgcolor="white",plot_bgcolor="white",legend_title_text="",yaxis_range=[0,100]); st.plotly_chart(fig,use_container_width=True)
    with right:
        heading("Competency profile","Ratings from the demo interview rubric.")
        labels=list(scores); vals=list(scores.values()); fig=go.Figure(go.Scatterpolar(r=vals+[vals[0]],theta=labels+[labels[0]],fill="toself",name="Candidate",line=dict(color="#3166a8",width=3),fillcolor="rgba(49,102,168,.16)")); fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,100])),showlegend=False,height=365,margin=dict(l=35,r=35,t=25,b=25),paper_bgcolor="white"); st.plotly_chart(fig,use_container_width=True)
        heading("Panel attention points")
        insight("1 · Validate ownership","Ask for the exact component, decisions and measurable impact personally delivered.")
        insight("2 · Test evaluation depth","Use a scenario that forces a precision/recall or latency/quality trade-off.")
        insight("3 · Inspect evidence fairly","Review CV alerts in context; do not infer misconduct from gaze or head movement alone.")
    heading("Suggested next step"); st.info("Consider a focused technical follow-up if the role requires applied ML. Validate project ownership and evaluation depth before deciding. This is decision support, not an automated hire/reject result.")

elif page=="Competency analysis":
    heading("Competency scorecard","Use the same rubric across candidates; tie notes to specific answers.")
    df=pd.DataFrame([{"Competency":k,"Score":v} for k,v in scores.items()]).sort_values("Score")
    fig=px.bar(df,x="Score",y="Competency",orientation="h",text="Score",color="Score",color_continuous_scale=["#d96b62","#e8bc61","#299b79"],range_color=[0,100]); fig.update_traces(texttemplate="%{text}/100",textposition="outside",cliponaxis=False); fig.update_layout(height=390,margin=dict(l=5,r=40,t=15,b=5),xaxis_range=[0,110],coloraxis_showscale=False,paper_bgcolor="white",plot_bgcolor="white"); st.plotly_chart(fig,use_container_width=True)
    st.caption("Demo guide: 90–100 consistently strong evidence; 75–89 good with small gaps; 60–74 mixed; below 60 insufficient evidence in this interview. Calibrate these bands with the hiring team.")
    chosen=st.selectbox("Inspect competency",list(details)); d=details[chosen]; st.markdown(f'### {chosen} · {scores[chosen]}/100'); st.write(d["summary"]); a,b=st.columns(2)
    with a:
        st.markdown("**Evidence observed**")
        for e in d["evidence"]: st.markdown(f"- {e}")
    with b: st.markdown("**Recommended follow-up**"); st.write(d["probe"])
    st.dataframe(df.sort_values("Score",ascending=False),use_container_width=True,hide_index=True)

elif page=="Pros & development areas":
    heading("Strengths and development areas","Keep observations job-related, specific and verifiable."); a,b=st.columns(2)
    with a:
        st.markdown("### 🟢 Strengths")
        for t,body in pros: insight(t,body,"#21a179")
    with b:
        st.markdown("### 🟠 Development areas / risks to validate")
        for t,body in cons: insight(t,body,"#d99a22")
    heading("Follow-up plan","Questions resolve evidence gaps; they should not confirm a pre-existing impression."); st.dataframe(pd.DataFrame(followups),use_container_width=True,hide_index=True)
    st.markdown("### Interviewer notes"); notes=st.text_area("Add human-reviewed notes",placeholder="Specific answer · evidence · context · follow-up needed",height=120)
    if st.button("Save notes to this session (demo only)"): st.success("Notes captured for this interaction only. Add secure persistence before production.")

elif page=="Integrity review":
    heading("Interview integrity review","Computer-vision signals are triage cues only. A flag is not a finding of cheating.")
    st.warning("Gaze/head changes can result from thinking, reading, camera placement, lighting or accessibility needs. Inspect the underlying evidence and applicable policy before drawing conclusions.")
    a,b,c,d=st.columns(4); a.metric("Photos analysed",f'{integrity["photos"]:,}'); b.metric("5-second windows",integrity["windows"]); c.metric("Gaze deviation windows",integrity["gaze"]); d.metric("Device detections",integrity["devices"])
    signals=pd.DataFrame([{ "Signal":"Face not detected","Windows":integrity["face_missing"],"Interpretation":"Occlusion, lighting or camera framing may explain it"},{"Signal":"Multiple people detected","Windows":integrity["multiple_people"],"Interpretation":"Check scene and camera context"},{"Signal":"Gaze deviation","Windows":integrity["gaze"],"Interpretation":"Can occur while thinking or reading"},{"Signal":"Head-position deviation","Windows":integrity["head"],"Interpretation":"May be normal movement or camera angle"},{"Signal":"Electronic device detection","Windows":integrity["devices"],"Interpretation":"Confirm object and whether use was permitted"}])
    fig=px.bar(signals.sort_values("Windows"),x="Windows",y="Signal",orientation="h",text="Windows",color="Windows",color_continuous_scale=["#9bb9dd","#d99a22"]); fig.update_layout(height=330,margin=dict(l=5,r=25,t=10,b=5),coloraxis_showscale=False,paper_bgcolor="white",plot_bgcolor="white"); st.plotly_chart(fig,use_container_width=True); st.dataframe(signals,use_container_width=True,hide_index=True)
    st.markdown("### Reviewer decision"); decision=st.radio("After inspecting evidence, choose a status",["Pending review","No concern after review","Needs further review","Policy concern substantiated by independent evidence"]); reason=st.text_area("Evidence and context (required for any concern)",placeholder="Timestamp · relevant frame/clip · policy rule · reviewer rationale")
    if st.button("Record review status (demo only)"):
        if decision in ["Needs further review","Policy concern substantiated by independent evidence"] and not reason.strip(): st.error("Provide evidence and context before recording a concern.")
        else: st.success(f"Demo status selected: {decision}. No persistent database is connected.")

elif page=="Interview evidence":
    heading("Answer-by-answer evidence","Replace these demo rows with transcript segments, timestamps and rubric annotations."); st.dataframe(questions,use_container_width=True,hide_index=True)
    fig=px.bar(questions,x="Question",y="Score",text="Score",color="Score",color_continuous_scale=["#d96b62","#e8bc61","#299b79"],range_color=[0,100]); fig.update_traces(textposition="outside"); fig.update_layout(height=330,margin=dict(l=5,r=15,t=15,b=5),yaxis_range=[0,110],coloraxis_showscale=False,paper_bgcolor="white",plot_bgcolor="white"); st.plotly_chart(fig,use_container_width=True)
    heading("Conversation-derived screening signals","Assess these from answers and examples—not face, voice, accent or personality assumptions.")
    for t,body in [("Technical depth","Explains why an approach was chosen, not only names tools."),("Reasoning structure","Defines the problem, states assumptions, compares options and checks results."),("Ownership and attribution","Separates personal work from team contributions."),("Evidence and impact","Supports claims with metrics, baselines, constraints or concrete outcomes."),("Learning agility","Responds constructively to hints and revises an approach when given new information."),("Business relevance","Connects technical choices to users, cost, latency, reliability or business goals."),("Consistency","Project descriptions stay coherent across follow-ups; discrepancies should be clarified, not presumed deceptive."),("Role-specific readiness","Demonstrates skills and practical judgement in the job rubric.")]: insight(t,body)
    st.markdown("### Transcript excerpt / interviewer evidence"); st.text_area("Paste a reviewed excerpt or note",placeholder="Timestamp · question · candidate answer · rubric evidence · reviewer note",height=140)
    st.caption("Avoid inferring honesty, motivation, mental health, personality or protected traits from facial expression, gaze, voice or other indirect signals.")

st.markdown('<div class="footer">CANDIDATE INTELLIGENCE · DEMO REPORT · HUMAN REVIEW REQUIRED · CONFIDENTIAL</div>',unsafe_allow_html=True)
