import streamlit as st
import analyzer

st.title('Resume Analyzer v2')
st.caption("Powered by Gemini, Groq, and CrewAI")
st.set_page_config(layout="wide", page_title="Resume Analyzer v2")

with st.form(key='my_form'):
    uploaded_resume = st.file_uploader("Upload Resume", type="pdf")
    submit = st.form_submit_button("Analyze")

if uploaded_resume:
    st.write(uploaded_resume)
    with st.spinner('Analyzing...'):
        pass
        # analyzer.resume_analysis_crew.kickoff(inputs={"resume": uploaded_resume})

else:
    st.error('Please upload a resume')