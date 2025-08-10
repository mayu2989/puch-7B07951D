import io
from fastapi import UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from PyPDF2 import PdfReader
from textblob import TextBlob
import spacy
import re

# Create a single FastAPI instance
app = FastAPI(title="Puch AI Hackathon Server")

nlp = spacy.load("en_core_web_sm")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ToolCall(BaseModel):
    name: str
    arguments: dict

class ToolResponse(BaseModel):
    content: list[dict]

# --- REQUIRED TOOL FOR PUCH AI HACKATHON ---
# The validate tool is required for authentication.
@app.post("/mcp/validate")
async def validate(bearer_token: dict):
   
    phone_number = "917020547381"

    return {"phone_number": phone_number}

# --- EXAMPLE TOOLS ---
# This endpoint handles the 'greet_user' tool.
@app.post("/mcp/suggest_music")
async def suggest_music_endpoint(tool_call: ToolCall):
    mood = tool_call.arguments.get("mood")
    
    if not mood:
        return {"content": [{"type": "text", "text": "Error: 'mood' argument is required."}]}
    
    # You can adapt the logic from your Streamlit app here.
    # For now, let's use a hardcoded version.
    MOOD_PLAYLISTS = {
        "happy": ["Pop Hits Playlist", "Dance Party Playlist"],
        "sad": ["Acoustic Chill Playlist", "Blues Classics Playlist"],
        "relaxed": ["Jazz Vibes Playlist", "Classical Music Playlist"],
        "angry": ["Rock Anthems Playlist", "Rap Battle Playlist"],
        "excited": ["EDM Bangers Playlist", "Hip-Hop Hits Playlist"]
    }

    playlists = MOOD_PLAYLISTS.get(mood.lower(), ["Pop Hits Playlist"])
    
    # Format the response for Puch AI
    response_text = f"Recommended Playlists for your {mood} mood: {', '.join(playlists)}"
    
    return {"content": [{"type": "text", "text": response_text}]}


def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(io.BytesIO(uploaded_file))
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

@app.post("/mcp/analyze_resume")
async def analyze_resume_endpoint(resume_file: UploadFile = File(...), job_description: str = Form(...)):
    try:
        # Read the uploaded PDF file
        resume_bytes = await resume_file.read()
        resume_text = extract_text_from_pdf(resume_bytes)

        if not resume_text:
            return {"content": [{"type": "text", "text": "Error: Could not extract text from resume."}]}
        if not job_description.strip():
            return {"content": [{"type": "text", "text": "Error: Job description is required."}]}
            
        # Perform the analysis using your functions
        match_score, overlap = get_keyword_match_score(resume_text, job_description)
        present_sections, missing_sections = check_sections(resume_text)
        corrections = grammar_corrections(resume_text)
        
        section_score = len(present_sections) / 5 * 100
        grammar_score = max(0, 100 - len(corrections) * 4)
        overall_score = get_resume_score(match_score, section_score, grammar_score)
        
        # Format the response for Puch AI
        response_text = (
            f"**Overall Resume Score:** {overall_score:.1f}/100\n"
            f"**Keyword Match:** {match_score:.1f}%\n"
            f"**Missing Sections:** {', '.join(missing_sections) if missing_sections else 'None'}\n"
            f"**Action Verbs:** {', '.join(extract_action_verbs(resume_text)[:5])}...\n"
        )
        
        return {"content": [{"type": "text", "text": response_text}]}

    except Exception as e:
        return {"content": [{"type": "text", "text": f"An error occurred: {str(e)}"}]}



app.mount("/", StaticFiles(directory="dist", html=True), name="static")

# --- RUNNING INSTRUCTIONS ---
# This is the main entry point to run the server.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)