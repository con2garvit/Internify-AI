import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="Resume Analyzer")

st.title("📄 AI Resume Analyzer")

mode = st.sidebar.selectbox(
    "Choose Feature",
    ["Resume Analyzer", "Resume Comparison"]
)

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

def extract_name(text):
    lines = text.split("\n")

    for line in lines[:5]:
        if len(line.split()) <= 4:
            return line.strip()

    return "Name Not Found"

def extract_email(text):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    emails = re.findall(pattern, text)

    if emails:
        return emails[0]

    return "Not Found"

def extract_phone(text):
    pattern = r'(\+?\d[\d\s\-]{8,15}\d)'
    phones = re.findall(pattern, text)

    if phones:
        return phones[0]

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

if mode == "Resume Analyzer":

 uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

 if uploaded_file is not None:

    text = extract_text(uploaded_file)
    name = extract_name(text)

    email = extract_email(text)

    phone = extract_phone(text)

    skills = extract_skills(text)

    score = calculate_score(email, skills)

    st.subheader("Analysis Result")
   
    st.write("👤 Name:", name)

    st.write("📧 Email:", email)

    st.write("📱 Phone:", phone)

    st.write("🛠 Skills Found:")
    if skills:
        for skill in skills:
            st.write("✓", skill)
    else:
        st.write("No skills detected")

    st.metric("ATS Score", f"{score}/100")

    if len(skills) < 5:
        st.warning("Add more technical skills.")

    if phone == "Not Found":
        st.warning("Phone number missing.")

    if email == "Not Found":
        st.warning("Email missing.")

    if len(skills) >= 5 and phone != "Not Found" and email != "Not Found":
       st.success("Your resume contains the basic information recruiters expect.")


    with st.expander("Resume Text"):
        st.write(text)



    if mode == "Resume Comparison":

     resume1 = st.file_uploader(
        "Upload Resume 1",
        type=["pdf"],
        key="resume1"
     )

     resume2 = st.file_uploader(
        "Upload Resume 2",
        type=["pdf"],
        key="resume2"
     )

     if resume1 and resume2:

        text1 = extract_text(resume1)
        text2 = extract_text(resume2)

        skills1 = extract_skills(text1)
        skills2 = extract_skills(text2)

        score1 = calculate_score(
            extract_email(text1),
            extract_phone(text1),
            skills1
        )

        score2 = calculate_score(
            extract_email(text2),
            extract_phone(text2),
            skills2
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Resume 1")
            st.metric("ATS Score", score1)
            st.write(skills1)

        with col2:
            st.subheader("Resume 2")
            st.metric("ATS Score", score2)
            st.write(skills2)
    
    