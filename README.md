# 🤝 MentorMatchAI

MentorMatchAI is an **AI-powered mentorship platform** that connects learners with experienced industry mentors.  
It combines **Streamlit (frontend)**, **FastAPI (backend)**, and **Supabase (database/auth)** to provide seamless mentor-mentee matching using **AI embeddings (Sentence Transformers)**.  

---

## 🚀 Features

 🔍 **AI-Powered Matching** → Matches mentees with mentors using semantic similarity (Sentence-BERT).  
 ⚡ **Skills-Based Pairing** → Connections based on specific skills, experience levels, and career goals.  
 📈 **Career Path Analysis** → Discover mentors who have walked similar journeys.  
 🎯 **Personalized Recommendations** → Tailored mentor suggestions based on profile and goals.  
 ⏰ **Flexible Scheduling** → Mentorship at times convenient across time zones.  
 ✅ **Verified Experts** → Only vetted mentors are listed.  
 🎨 **Modern UI** → Dark-themed, interactive Streamlit frontend with smooth UX.  

---

## 📂 Project Structure
MentorMatchAI/
- │── backend/
- │   └── app/
- │       └── main.py              # FastAPI backend (mentor matching, add mentor, etc.)
- │── frontend/
- │   └── streamlit_app.py         # Streamlit frontend (UI/UX, mentor forms, listings)
- │── mentor_match.db              # SQLite / Supabase DB (if local testing)
- │── .env                         # Environment variables (Supabase credentials, API URL)
- │── .gitignore                   # Ignored files (env, cache, IDE, etc.)
- │── README.md                    # Project documentation

---

## 🛠️ Tech Stack

### Frontend
- [Streamlit](https://streamlit.io/) → Interactive frontend UI  
- Custom HTML/CSS → For enhanced design  

### Backend
- [FastAPI](https://fastapi.tiangolo.com/) → REST API framework  
- [Sentence Transformers](https://www.sbert.net/) → AI-based similarity scoring  

### Database
- [Supabase](https://supabase.com/) → Postgres DB + Authentication  
- SQLite (optional for local testing)  

### Other Tools
- Python 3.9+  
- dotenv (for `.env` config)  
- Requests (for API calls)  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
git clone https://github.com/rashmitharaka1/MentorMatchAI.git
cd MentorMatchAI

### 2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

### 3️⃣ Install Dependencies
pip install -r requirements.txt

If no requirements.txt, install manually:
pip install streamlit fastapi uvicorn supabase python-dotenv sentence-transformers requests

### 4️⃣ Configure Environment Variables
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
API_URL=http://127.0.0.1:8000

---
## ▶️ Running the Project
### Run Backend (FastAPI)
uvicorn backend.app.main:app --reload

Server will start at: http://127.0.0.1:8000

### Run Frontend (Streamlit)
streamlit run frontend/streamlit_app.py

Frontend will start at: http://localhost:8501

---
## 📡 API Endpoints

| Method | Endpoint       | Description                   |
|--------|---------------|-------------------------------|
| GET    | `/`           | Health check (API running)    |
| POST   | `/add-mentor` | Add new mentor to database    |
| POST   | `/match-mentor` | Match mentee with best mentors |
