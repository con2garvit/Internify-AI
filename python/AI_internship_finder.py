import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="Resume Analyzer")

st.title("📄 AI Resume Analyzer")

# Skill database
SKILLS_DB = [
    "python",
    "pandas",
    "numpy",
    "sql",
    "mongodb",
    "html",
    "css",
    "javascript",
    "git",
    "github",
    "streamlit",
    "machine learning",
    "data analysis",
    "java",
    "c++"
]

def extract_text(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text

def extract_email(text):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    emails = re.findall(pattern, text)

    if emails:
        return emails[0]

    return "Not Found"

def extract_skills(text):
    found_skills = []

    text = text.lower()

    for skill in SKILLS_DB:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills

def calculate_score(email, skills):
    score = 0

    if email != "Not Found":
        score += 20

    score += min(len(skills) * 8, 80)

    return min(score, 100)

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file is not None:

    text = extract_text(uploaded_file)

    email = extract_email(text)

    skills = extract_skills(text)

    score = calculate_score(email, skills)

    st.subheader("Analysis Result")

    st.write("📧 Email:", email)

    st.write("🛠 Skills Found:")
    if skills:
        for skill in skills:
            st.write("✓", skill)
    else:
        st.write("No skills detected")

    st.metric("ATS Score", f"{score}/100")

    with st.expander("Resume Text"):
        st.write(text)