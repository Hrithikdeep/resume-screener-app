import os
import streamlit as st
import pdfplumber
from groq import Groq

# 🔐 Set your Groq API key here
import streamlit as st
GROQ_API_KEY = st.secrets["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"]

client = Groq(api_key=GROQ_API_KEY)

# ✅ Streamlit Setup
st.set_page_config(page_title="AI Resume Screener (Strict)", layout="wide")
st.title("🧠 AI Resume Screener (Strict ATS Version)")
st.markdown("Upload your resume PDF and paste the job description to get a brutally honest U.S. recruiter-level evaluation.")

# 📤 Resume Upload
uploaded_file = st.file_uploader("📄 Upload Resume (PDF Only)", type=["pdf"])

# 📌 JD Input
job_description = st.text_area("📌 Paste Job Description Here", height=200)

resume_text = ""

# 🧾 Extract Resume Text from PDF
if uploaded_file is not None:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            resume_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        st.success("✅ Resume extracted successfully!")
    except:
        st.error("❌ Failed to extract text from PDF. Make sure it's not scanned image.")

# 🚀 When both resume + JD provided
if resume_text and job_description:
    if st.button("🔍 Analyze Resume (Strict Mode)"):
        with st.spinner("Analyzing with Groq AI..."):

            # 🧠 Strict U.S. ATS Recruiter Prompt
            prompt = f"""
You are acting as a strict ATS + U.S. Recruiter.

You must:
- Critically analyze the resume and compare it to the job description
- Highlight missing skills, wrong project alignment, and scoring penalties
- DO NOT praise or pass weak resumes
- Be brutally honest like a recruiter who only selects top 5% candidates

Give your feedback ONLY in the 5 sections below:

---

1️⃣ **Resume Score & Verdict (0–100)**:
Strictly score the resume. Is it likely to be shortlisted or rejected? Why?

2️⃣ **Key Skills Missing**:
List all technical + soft skills/tools mentioned in JD that are missing from resume.

3️⃣ **Wrong or Missing Projects**:
Does resume have projects matching the JD? If not, suggest 2–3 realistic projects.

4️⃣ **Resume Format/Impact Issues**:
Mention if format is bad, bullet points missing, no action verbs, or lacks results.

5️⃣ **Section-wise Fix Suggestions**:
Suggest improvements like:
- Skills: Add Python, SQL
- Projects: Replace image classifier with GenAI chatbot
- Experience: Add 1 line showing metrics

---

Job Description:
\"\"\"{job_description}\"\"\"

Resume:
\"\"\"{resume_text}\"\"\"
"""

            # 🔄 Groq API Call
            try:
                response = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )

                result = response.choices[0].message.content
                st.markdown("---")
                st.subheader("📊 Screening Result")
                st.markdown(result)

            except Exception as e:
                st.error(f"❌ Error from Groq API: {e}")
else:
    st.info("Please upload resume PDF and paste job description to begin.")




