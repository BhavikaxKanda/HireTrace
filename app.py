import streamlit as st
import os
import base64
from PIL import Image
from utils.pdf_parser import extract_text_from_pdf
from utils.pii_masker import mask_pii
from agents.parser import extract_jd_requirements
from agents.scorer import score_candidate

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="HireTrace AI", layout="wide")

def get_base64_logo(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- CSS FOR MODERN UI, GLITTER BUTTON, AND SHIMMER TITLE ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #0E1117; color: #FFFFFF; }
    
    /* HIDE THEME SWITCHER (LIGHT/DARK/SYSTEM) IN MENU */
    div[data-testid="stStatusWidget"] { display: none; }
    #MainMenu { visibility: visible; }
    button[title="View menu"] + div div ul li:first-child { display: none; }

    /* GLITTERING WHITE TITLE EFFECT */
    .main-title { 
        font-family: 'Segoe UI', sans-serif; 
        font-weight: 800; 
        font-size: 3.5rem; 
        margin: 0;
        line-height: 1.1;
        background: linear-gradient(90deg, #FFFFFF, #8B949E, #FFFFFF);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glitter 3s linear infinite;
    }
    
    /* GLITTER & ANIMATED BUTTON */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #00FFFF, #008080, #00FFFF);
        background-size: 200% auto;
        color: #0E1117; 
        font-weight: bold; 
        border: none; 
        border-radius: 5px; 
        padding: 0.6rem 2rem; 
        width: 100%;
        animation: glitter 3s linear infinite;
        transition: 0.3s;
    }
    
    @keyframes glitter {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    
    div.stButton > button:first-child:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px #00FFFF66;
    }

    .final-score-box { border: 1px solid #00FFFF; padding: 15px; border-radius: 10px; text-align: center; background-color: #161B22; }
    .justified-text { text-align: justify; line-height: 1.6; font-size: 0.95rem; color: #E6EDF3; }
    .dim-header { color: #00FFFF; font-weight: bold; border-bottom: 1px solid #30363D; margin-bottom: 5px; }
    
    .cyan-score { color: #00FFFF; font-weight: bold; font-family: 'Courier New', monospace; }
</style>
""", unsafe_allow_html=True)

# --- 2. HEADER SECTION (Logo + Shimmer Title) ---
try:
    logo_base = get_base64_logo("logohrai.png")
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 25px; margin-top: -20px;">
            <img src="data:image/png;base64,{logo_base}" width="220">
            <div style="display: flex; flex-direction: column; justify-content: center;">
                <h1 class='main-title'>HireTrace AI</h1>
                <p style='color: #8B949E; font-size: 1.2rem; margin: 0; padding-top: 0px;'>
                    AI-Powered Semantic Shortlisting & Bias-Free Ranking Agent
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
except:
    st.title("HireTrace AI")

st.markdown("---")

# --- 3. JOB DESCRIPTION SECTION ---
st.subheader("1. Job Description")
jd_method = st.radio("Input method:", ("Paste Text", "Upload PDF"), horizontal=True)
jd_text = ""
if jd_method == "Paste Text":
    jd_text = st.text_area("Paste JD:", height=200)
else:
    jd_file = st.file_uploader("Upload JD PDF", type="pdf")
    if jd_file:
        with open("temp_jd.pdf", "wb") as f: f.write(jd_file.getbuffer())
        jd_text = extract_text_from_pdf("temp_jd.pdf")
        os.remove("temp_jd.pdf")
        st.success("✅ Job Description uploaded successfully.")

# --- 4. RESUME UPLOAD SECTION ---
st.subheader("2. Upload Resumes")
uploaded_files = st.file_uploader("Select PDF resumes", type="pdf", accept_multiple_files=True)

def calculate_total(dims):
    weights = {
        "Skills Match": 0.30, 
        "Experience Relevance": 0.25, 
        "Education & Certs": 0.15, 
        "Project/Portfolio": 0.20, 
        "Communication Quality": 0.10
    }
    
    total = 0
    for k, w in weights.items():
        if k in dims:
            score = float(dims[k]['score'])
            if score <= 1.0: score *= 10 # Scaling safety
            total += min(score, 10) * w
            
    return round(total, 2)

# --- 5. RANKING ENGINE ---
if st.button("START ANALYZING"):
    if jd_text and uploaded_files:
        with st.spinner("Analyzing candidates..."):
            jd_specs = extract_jd_requirements(jd_text)
            results = []
            for file in uploaded_files:
                with open(file.name, "wb") as f: f.write(file.getbuffer())
                raw_text = extract_text_from_pdf(file.name)
                masked_text = mask_pii(raw_text)
                analysis = score_candidate(jd_specs, masked_text)
                analysis['Candidate Name'], analysis['total_score'] = file.name, calculate_total(analysis['dimensions'])
                results.append(analysis)
                os.remove(file.name)

            st.markdown("---")
            st.subheader("📊 Ranking of Shortlisted Candidates")
            for res in sorted(results, key=lambda x: x['total_score'], reverse=True):
                with st.expander(f"👤 {res['Candidate Name']} — {res['total_score']}/10", expanded=True):
                    c1, c2 = st.columns([1, 4])
                    with c1:
                        st.markdown(f"<div class='final-score-box'><h2 style='color: #00FFFF; margin:0;'>{res['total_score']}</h2></div>", unsafe_allow_html=True)
                        if res['total_score'] >= 7.5: st.success("✅ HIGHLY RECOMMEND")
                        elif res['total_score'] >= 6.5: st.warning("⚠️ CONSIDER")
                        else: st.error("❌ DO NOT HIRE")
                    with c2:
                        st.markdown(f"**AI Audit Summary:** {res.get('overall_summary', 'N/A')}")
                        h1, h2, h3 = st.columns([1.5, 1, 4])
                        h1.markdown("<div class='dim-header'>Dimension</div>", unsafe_allow_html=True)
                        h2.markdown("<div class='dim-header'>Score</div>", unsafe_allow_html=True)
                        h3.markdown("<div class='dim-header'>Justification</div>", unsafe_allow_html=True)
                        for dim, data in res['dimensions'].items():
                            d1, d2, d3 = st.columns([1.5, 1, 4])
                            d1.write(f"**{dim}**")
                            row_score = float(data['score'])
                            if row_score <= 1.0: row_score *= 10
                            d2.markdown(f"<span class='cyan-score'>{round(row_score, 1)}/10</span>", unsafe_allow_html=True)
                            d3.markdown(f"<div class='justified-text'>{data['justification']}</div>", unsafe_allow_html=True)
                            st.markdown("<div style='border-bottom: 1px solid #30363D; margin: 5px 0;'></div>", unsafe_allow_html=True)