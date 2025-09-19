from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

app = FastAPI(title="MentorMatchAI API 🚀")

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

class TextPair(BaseModel):
    text1: str
    text2: str

@app.get("/")
def home():
    return {"message": "MentorMatchAI Backend is running 🚀"}

@app.post("/similarity")
def similarity(data: TextPair):
    emb1 = model.encode(data.text1, convert_to_tensor=True)
    emb2 = model.encode(data.text2, convert_to_tensor=True)
    score = util.pytorch_cos_sim(emb1, emb2).item()
    return {"similarity_score": round(score, 4)}
