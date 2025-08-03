import streamlit as st

st.title('Resume Analyzer v2')
st.caption("Powered by Gemini, Groq, and CrewAI")
st.set_page_config(layout="wide", page_title="Resume Analyzer v2")

with st.form(key='my_form'):
    uploaded_resume = st.file_uploader("Upload Resume", type="pdf")
    submit = st.form_submit_button("Analyze")

if uploaded_resume is not None:
    with st.spinner('Analyzing...'):
        pass

else:
    st.error('Please upload a resume')