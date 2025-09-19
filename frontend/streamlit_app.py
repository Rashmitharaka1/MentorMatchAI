import streamlit as st
import requests

# ----------------------------
# Config
# ----------------------------
API_URL = "http://127.0.0.1:8000"  # Backend API URL

st.set_page_config(
    page_title="MentorMatchAI",
    page_icon="🤝",
    layout="wide",
)

# ----------------------------
# Hero Section (Landing Page)
# ----------------------------
st.markdown(
    """
    <style>
        .hero {
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(120deg, #6a11cb, #2575fc);
            border-radius: 12px;
            color: white;
        }
        .hero h1 {
            font-size: 48px;
            font-weight: bold;
        }
        .highlight {
            color: #FFD700;  /* Yellow highlight */
        }
        .stats {
            display: flex;
            justify-content: center;
            margin-top: 30px;
            gap: 50px;
        }
        .stat {
            text-align: center;
        }
        .btn-container {
            margin-top: 25px;
        }
    </style>
    <div class="hero">
        <h1>Find Your Perfect <span class="highlight">AI-Matched Mentor</span></h1>
        <p>Connect with industry experts who match your skills, goals, and career aspirations 
        through our advanced AI matching system.</p>
        <div class="btn-container">
            <a href="#similarity" target="_self">
                <button style="padding:10px 25px; font-size:16px; border:none; border-radius:8px; background:#FFD700; color:black; font-weight:bold; cursor:pointer;">
                    Find My Mentor
                </button>
            </a>
            <a href="#become" target="_self">
                <button style="padding:10px 25px; font-size:16px; border:2px solid white; border-radius:8px; background:transparent; color:white; font-weight:bold; cursor:pointer; margin-left:15px;">
                    Become a Mentor
                </button>
            </a>
        </div>
        <div class="stats">
            <div class="stat">
                <h2>5000+</h2>
                <p>Active Mentors</p>
            </div>
            <div class="stat">
                <h2>98%</h2>
                <p>Match Accuracy</p>
            </div>
            <div class="stat">
                <h2>15k+</h2>
                <p>Successful Connections</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")

# ----------------------------
# Mentor Matching Section
# ----------------------------
st.header("🔎 Try Mentor Matching")
st.write("Enter two short bios (mentee & mentor) to check similarity:")

text1 = st.text_area("Enter first text (mentee bio)", "", key="text1")
text2 = st.text_area("Enter second text (mentor bio)", "", key="text2")

if st.button("Check Similarity", key="check_btn"):
    if text1.strip() and text2.strip():
        with st.spinner("Calculating similarity..."):
            try:
                response = requests.post(f"{API_URL}/similarity", json={"text1": text1, "text2": text2})
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✅ Similarity Score: **{result['similarity_score']}**")
                else:
                    st.error("❌ Error from backend API")
            except Exception as e:
                st.error(f"⚠️ Connection error: {e}")
    else:
        st.warning("⚠️ Please enter both texts to compare.")

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.caption("🚀 Powered by [Sentence Transformers](https://www.sbert.net/) | Built with Streamlit & FastAPI")
