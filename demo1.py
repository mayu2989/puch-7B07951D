import streamlit as st
from PyPDF2 import PdfReader
import spacy
from textblob import TextBlob
import re

st.set_page_config(page_title="AI Resume Reviewer", layout="wide")
st.title("AI Resume Reviewer")

nlp = spacy.load("en_core_web_sm")

soft_skills = [
    'communication', 'leadership', 'teamwork', 'problem solving', 'adaptability',
    'creativity', 'time management', 'work ethic'
]
hard_skills = [
    'python', 'sql', 'excel', 'machine learning', 'data analysis',
    'react', 'django', 'javascript', 'c++', 'java'
]

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        piece = page.extract_text()
        if piece:
            text += piece
    return text or ""

def extract_keywords(text):
    doc = nlp(text)
    keywords = set(token.lemma_.lower() for token in doc if token.pos_ in ['NOUN', 'PROPN', 'VERB'])
    return keywords

def get_keyword_match_score(resume_text, job_desc):
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_desc)
    if not job_keywords:
        return 0, set()
    match_score = len(resume_keywords & job_keywords) / len(job_keywords) * 100
    overlap = resume_keywords & job_keywords
    return match_score, overlap

def check_sections(resume_text):
    sections = ['contact', 'skill', 'experience', 'education', 'project']
    present = [s for s in sections if s in resume_text.lower()]
    missing = [s for s in sections if s not in resume_text.lower()]
    return present, missing

def grammar_corrections(resume_text, max_sents=6):
    sents = list(nlp(resume_text).sents)
    corrections = []
    for sent in sents[:max_sents]:
        orig = sent.text.strip()
        corrected = str(TextBlob(orig).correct())
        if orig and corrected and orig != corrected:
            corrections.append((orig, corrected))
    return corrections

def highlight_nonquantifiable(text):
    lines = text.split('\n')
    nonquant = [line for line in lines if line.strip() and not re.search(r'\d', line)]
    return nonquant

def extract_action_verbs(resume_text):
    return list(set(token.lemma_ for token in nlp(resume_text) if token.pos_ == "VERB" and not token.is_stop))

def get_resume_score(match_score, section_score, grammar_score):
    return round((match_score + section_score + grammar_score) / 3, 1)

def extract_skills(resume_text, skill_list):
    found = [skill for skill in skill_list if skill.lower() in resume_text.lower()]
    return found

def detect_email(resume_text):
    match = re.search(r'\b[\w.-]+?@\w+?\.\w+?\b', resume_text)
    return match.group() if match else "Not found"

def detect_phone(resume_text):
    match = re.search(r'\b[789]\d{9}\b', resume_text)
    return match.group() if match else "Not found"

def job_missing_keywords(resume_text, job_desc):
    resume_kw = extract_keywords(resume_text)
    job_kw = extract_keywords(job_desc)
    missing = [kw for kw in job_kw if kw not in resume_kw]
    return missing

# --- UI ---
uploaded_file = st.file_uploader("**Upload your Resume (PDF format):**", type=["pdf"])
job_desc = st.text_area("**Paste the target Job Description here:**", height=150)

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.subheader("Extracted Resume Text")
    st.write(resume_text if resume_text else "(Could not extract PDF text)")

    if job_desc.strip():
        st.subheader("Analysis Results")
        # Keyword Match
        match_score, overlap = get_keyword_match_score(resume_text, job_desc)
        st.markdown(f"**Keyword Match Score:** `{match_score:.1f}%`")
        st.markdown(f"**Matching Keywords:** `{', '.join(overlap)}`" if overlap else "_No overlap_")

        # Section Check
        present, missing = check_sections(resume_text)
        section_score = len(present) / 5 * 100
        st.markdown(f"**Sections Present:** `{', '.join(present)}`")
        st.markdown(f"**Sections Missing:** `{', '.join(missing)}`" if missing else "All sections present")

        # Skills extraction
        ss_found = extract_skills(resume_text, soft_skills)
        hs_found = extract_skills(resume_text, hard_skills)
        st.markdown(f"**Soft Skills Detected:** `{', '.join(ss_found)}`" if ss_found else "No soft skills detected.")
        st.markdown(f"**Hard Skills Detected:** `{', '.join(hs_found)}`" if hs_found else "No hard skills detected.")

        # Contact info
        email = detect_email(resume_text)
        phone = detect_phone(resume_text)
        st.markdown(f"**Detected Email:** `{email}`")
        st.markdown(f"**Detected Phone:** `{phone}`")

        # Grammar suggestions
        st.subheader("Grammar & Spelling Suggestions (TextBlob)")
        corrections = grammar_corrections(resume_text)
        if corrections:
            for orig, corrected in corrections:
                st.write(f"Original: {orig}")
                st.write(f"Suggestion: {corrected}")
                st.write("---")
        else:
            st.write("No major grammar improvements found.")

        # Quantifiable Achievements
        no_num_bullets = highlight_nonquantifiable(resume_text)
        st.subheader("Achievements to Quantify")
        if no_num_bullets:
            for bullet in no_num_bullets[:8]:
                st.write(f"→ {bullet}")
        else:
            st.write("All achievements appear to be quantifiable.")

        # Action verbs
        action_verbs = extract_action_verbs(resume_text)
        st.markdown(f"**Action Verbs Used:** `{', '.join(action_verbs)}`")

        # Gap analysis
        missing_keywords = job_missing_keywords(resume_text, job_desc)
        st.subheader("Missing Keywords/Requirements from Resume")
        if missing_keywords:
            st.write(', '.join(missing_keywords))
        else:
            st.write("All major requirements covered!")

        # Scores
        grammar_score = max(0, 100 - len(corrections) * 4)
        overall_score = get_resume_score(match_score, section_score, grammar_score)
        st.markdown(f"### 🏆 Overall Resume Score: `{overall_score}` / 100")

    else:
        st.info("Paste a job description to compare keywords and fit.")

else:
    st.info("Please upload your resume and paste the job description for analysis.")

st.caption("Built for Puch AI Hackathon | No Java | With extra features!")
