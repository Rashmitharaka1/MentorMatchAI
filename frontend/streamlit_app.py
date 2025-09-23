# app.py
import os
import math
import streamlit as st
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

# ---- load env ----
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("❌ Supabase credentials not found. Check your .env file (SUPABASE_URL, SUPABASE_KEY).")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---- page config ----
st.set_page_config(page_title="MentorMatchAI", page_icon="🤝", layout="wide")

# ---- session state ----
if "show_section" not in st.session_state:
    st.session_state.show_section = "home"

# ---- helper: fetch mentors ----
def fetch_all_mentors(limit=1000):
    try:
        resp = supabase.table("mentors").select("*").order("id", desc=False).limit(limit).execute()
        return resp.data or []
    except Exception as e:
        return e

# ---- UI: Home / Hero ----
if st.session_state.show_section == "home":
    st.markdown("""
        <style>
        /* Page background */
        body, .main, .block-container {
            background-color: #000000;  /* black background */
            color: #ffffff;             /* default text white */
        }
        .hero { text-align: center; padding: 80px 20px; border-radius: 12px; width: 100%; }
        .hero h1 { font-size: 55px; font-weight: 700; margin-bottom: 8px; color: #E6E6FA; }
        .hero p { font-size: 18px; color: #E6E6FA; }
        .buttons-row > div { padding: 0 8px; } /* reduce spacing between buttons */
        .why-section { margin-top: 180px; text-align: center; } /* move Why Choose section down */

        /* Card hover transitions */
        .card {
            background:#4B0082;
            border-radius:12px;
            margin:16px;
            padding:16px;
            color:#fff;
            height:250px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        }

        .mentor-card {
            background:#4B0082;
            border-radius:12px;
            margin:16px;
            padding:16px;
            color:#fff;
            height:250px;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .mentor-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        }
        </style>

        <div class="hero">
            <h1>Find Your Perfect <span style="color:#6a3fb5">AI-Matched Mentor</span></h1>
            <p>Connect with industry experts who match your skills and career goals.</p>
        </div>
    """, unsafe_allow_html=True)

    # --- navigation buttons (in one row) ---
    c1, c2, c3, c4 = st.columns([4,2,2,4])
    with c2:
        if st.button("🔍 Find My Mentor", use_container_width=True, key="find_btn"):
            st.session_state.show_section = "find"
            st.rerun()
    with c3:
        if st.button("🧑‍🏫 Become a Mentor", use_container_width=True, key="become_btn"):
            st.session_state.show_section = "become"
            st.rerun()

    # ---- Why Choose MentorMatchAI? ----
    st.markdown("""
        <div class="why-section">
            <h2>💡 Why Choose MentorMatchAI?</h2>
        </div>
    """, unsafe_allow_html=True)

    features = [
        ("🔍", "AI-Powered Matching", "Advanced algorithms analyze your profile and match you with mentors who truly fit your goals."),
        ("⚡", "Skills-Based Pairing", "Connections based on specific skills, experience levels, and career paths, and professional development goals."),
        ("📈", "Career Path Analysis", "Find mentors who have walked similar career paths and gained valuable experience in your industry."),
        ("🎯", "Personalized Recommendations", "Mentor suggestions carefully tailored to your learning style, career goals, and professional background."),
        ("⏰", "Flexible Scheduling", "Book mentorship sessions at convenient times that work for you, across different time zones."),
        ("✅", "Verified Experts", "All mentors are carefully vetted professionals with proven experience and successful track records.")
    ]
    cols_per_row = 3
    rows = math.ceil(len(features) / cols_per_row)
    for r in range(rows):
        cols = st.columns(cols_per_row)
        for c_idx in range(cols_per_row):
            idx = r * cols_per_row + c_idx
            if idx >= len(features):
                break
            icon, title, desc = features[idx]
            with cols[c_idx]:
                st.markdown(
                    f"""
                    <div class="card">
                      <div style="font-size:30px;margin-bottom:6px;text-align:center;">{icon}</div>
                      <h4 style="margin:0 0 6px 0">{title}</h4>
                      <p style="margin:0">{desc}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ---- Meet Our Mentors ----
    mentors = fetch_all_mentors(limit=1000)
    if isinstance(mentors, Exception):
        st.error(f"❌ Error fetching mentors: {mentors}")
    else:
        st.markdown("""
        <div class="why-section">
            <h2>🌟 Meet Our Mentors</h2>
        </div>
        <div style="text-align:center;margin-bottom:20px;"> """, unsafe_allow_html=True)
        if not mentors:
            st.info("ℹ️ No mentors available yet. Add mentors using the 'Become a Mentor' form above.")
        else:
            cols_per_row = 3
            rows = math.ceil(len(mentors) / cols_per_row)
            for r in range(rows):
                cols = st.columns(cols_per_row)
                for c_idx in range(cols_per_row):
                    idx = r * cols_per_row + c_idx
                    if idx >= len(mentors):
                        break
                    m = mentors[idx]
                    name = m.get("name", "Unknown")
                    expertise = m.get("expertise", "")
                    email = m.get("email", "")
                    with cols[c_idx]:
                        st.markdown(
                            f"""
                            <div class="mentor-card">
                              <h3 style="margin:0 0 6px 0">{name}</h3>
                              <p style="margin:0 0 6px 0"><strong>Expertise:</strong> {expertise}</p>
                              <p style="margin:0 0 8px 0"><strong>Email:</strong> {email or 'Not provided'}</p>
                              <a href="mailto:{email}" style="display:inline-block;margin-top:6px;padding:7px 10px;background:#FFD700;color:#000;border-radius:6px;text-decoration:none;font-weight:600;">
                                Contact Now
                              </a>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

# ---- Become a Mentor ----
elif st.session_state.show_section == "become":
    # Apply black theme CSS
    st.markdown("""
        <style>
            .main, .block-container, body {
                background-color: #000000 !important;
                color: #ffffff !important;
            }
            input, textarea, .stButton button {
                background-color: #1a1a1a !important;
                color: #ffffff !important;
            }
            .stButton button:hover {
                background-color: #3333ff !important;
                color: #ffffff !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Top-left "arrow"
    back_col, _ = st.columns([0.1, 10])
    with back_col:
        if st.button("⬅ ", key="back_btn"):
            st.session_state.show_section = "home"
            st.rerun()

    st.title("🧑‍🏫 Become a Mentor")
    with st.form("mentor_form"):
        name = st.text_input("Your Name *")
        expertise = st.text_input("Expertise (comma separated)")
        bio = st.text_area("Short Bio *")
        email = st.text_input("Email *")
        submitted = st.form_submit_button("Add Mentor")
        if submitted:
            if not (name and bio and email):
                st.warning("⚠️ Please fill name, bio, and email.")
            else:
                try:
                    supabase.table("mentors").insert({
                        "name": name,
                        "expertise": expertise,
                        "bio": bio,
                        "email": email
                    }).execute()
                    st.success("✅ Mentor added successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to add mentor: {e}")


# ---- Find My Mentor ----
elif st.session_state.show_section == "find":
    # Apply black theme CSS
    st.markdown("""
        <style>
            .main, .block-container, body {
                background-color: #000000 !important;
                color: #ffffff !important;
            }
            input, textarea, .stButton button {
                background-color: #1a1a1a !important;
                color: #ffffff !important;
            }
            .stButton button:hover {
                background-color: #3333ff !important;
                color: #ffffff !important;
            }
        </style>
    """, unsafe_allow_html=True)

    back_col, _ = st.columns([0.1, 10])
    with back_col:
        if st.button("⬅ ", key="back_btn"):
            st.session_state.show_section = "home"
            st.rerun()
    st.title("🔍 Find My Mentor")
    prompt = st.text_area("Describe your career goals, skills, or what kind of mentor you want:")
    if st.button("Match Me with Mentors"):
        if not prompt.strip():
            st.warning("⚠️ Please enter a prompt.")
        else:
            try:
                resp = requests.post(f"{API_URL}/match-mentor", json={"prompt": prompt}, timeout=20)
            except Exception as e:
                st.error(f"❌ Error contacting match API: {e}")
            else:
                if resp.status_code != 200:
                    st.error(f"❌ Match API error: {resp.status_code} {resp.text}")
                else:
                    data = resp.json()
                    matches = data.get("matches", [])
                    if not matches:
                        st.info("⚠️ No matches returned.")
                    else:
                        matches_sorted = sorted(matches, key=lambda x: x.get("score", 0), reverse=True)
                        st.success(f"✅ Found {len(matches_sorted)} matches (sorted by score)")
                        for m in matches_sorted:
                            name = m.get("name", "Unknown")
                            expertise = m.get("expertise", "")
                            bio = m.get("bio", "")
                            email = m.get("email", "")
                            score = m.get("score", None)
                            score_text = f"{score:.2f}" if isinstance(score, (int, float)) else str(score)
                            st.markdown(f"### {name} — score: **{score_text}**")
                            st.write(f"**Expertise:** {expertise}")
                            st.write(f"**Bio:** {bio}")
                            
