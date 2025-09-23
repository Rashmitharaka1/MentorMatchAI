from dotenv import load_dotenv
import os
from pathlib import Path

# Go three levels up from main.py (backend/app → MentorMatchAI root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
dotenv_path = BASE_DIR / ".env"

# Debug check
print("Looking for .env at:", dotenv_path)
print("Exists?", dotenv_path.exists())

# Load .env
load_dotenv(dotenv_path=dotenv_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_KEY:", "SET" if SUPABASE_KEY else "None")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE_URL or SUPABASE_KEY is missing. Check your .env file.")

from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="MentorMatchAI API 🚀")

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Pydantic models
class Mentor(BaseModel):
    name: str
    bio: str
    expertise: str = ""
    email: str

class UserPrompt(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "MentorMatchAI Backend is running 🚀"}

@app.post("/add-mentor")
def add_mentor(mentor: Mentor):
    data = {
        "name": mentor.name,
        "bio": mentor.bio,
        "expertise": mentor.expertise,
        "email": mentor.email
    }
    response = supabase.table("mentors").insert(data).execute()
    return {"message": "Mentor added", "data": response.data}

@app.post("/match-mentor")
def match_mentor(user: UserPrompt):
    # Get all mentors
    mentors = supabase.table("mentors").select("*").execute().data
    if not mentors:
        return {"matches": []}

    # Encode user prompt
    user_emb = model.encode(user.prompt, convert_to_tensor=True)

    results = []
    for m in mentors:
        mentor_emb = model.encode(m["bio"], convert_to_tensor=True)
        score = util.pytorch_cos_sim(user_emb, mentor_emb).item()
        results.append({
            "id": m["id"],
            "name": m["name"],
            "bio": m["bio"],
            "expertise": m.get("expertise", ""),
            "score": round(score, 4)
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return {"matches": results[:3]}  # top 3 matches
