# app.py
import streamlit as st
import base64
import requests
import os
import json
from PIL import Image
import io

# ---------------- CONFIG ----------------
REPO_OWNER = "its0su0rj"
REPO_NAME  = "owspracticeits-suraj"
BRANCH     = "main"

RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/"

st.set_page_config(page_title="For You ❤️", layout="wide")

# -------------- HELPERS ---------------

def raw_url(path):
    return RAW_BASE + path

def fetch_bytes(path):
    try:
        r = requests.get(raw_url(path))
        if r.status_code == 200:
            return r.content
    except:
        pass
    return None

def show_image(path):
    img_bytes = fetch_bytes(path)
    if img_bytes:
        img = Image.open(io.BytesIO(img_bytes))
        st.image(img, use_column_width=True)

def play_audio(path):
    audio_bytes = fetch_bytes(path)
    if audio_bytes:
        st.audio(audio_bytes, format="audio/mp3")

# -------------- SESSION ---------------
if "stage" not in st.session_state:
    st.session_state.stage = "proposal"

# =====================================================
# 💘 STAGE 1 — PROPOSAL PAGE
# =====================================================

if st.session_state.stage == "proposal":

    html = """
    <style>
    body {
        background: linear-gradient(135deg,#fff0f5,#ffe6f0);
    }
    .container {
        text-align:center;
        padding-top:80px;
    }
    .title {
        font-size:36px;
        font-weight:800;
        color:#ff2d6f;
        margin-bottom:40px;
    }
    .btn {
        padding:14px 30px;
        font-size:20px;
        border:none;
        border-radius:14px;
        cursor:pointer;
        margin:10px;
        transition:0.2s ease;
    }
    .yes {
        background:#ff4d6d;
        color:white;
    }
    .no {
        background:#444;
        color:white;
        position:absolute;
    }
    </style>

    <div class="container">
        <div class="title">
            Nirali… will you be my Valentine? 💖
        </div>

        <button class="btn yes" onclick="window.parent.postMessage('YES_CLICKED','*')">Yes 💘</button>
        <button class="btn no" id="noBtn">No 😢</button>
    </div>

    <script>
    const noBtn = document.getElementById("noBtn");

    noBtn.addEventListener("mouseover", function(){
        const x = Math.random()*400 - 200;
        const y = Math.random()*200 - 100;
        noBtn.style.transform = `translate(${x}px, ${y}px)`;
    });
    </script>
    """

    st.components.v1.html(html, height=500)

    # Listen for YES click
    if st.button("I CLICKED YES ❤️"):
        st.session_state.stage = "love"
        st.rerun()

# =====================================================
# 💕 STAGE 2 — LOVE EXPERIENCE PAGE
# =====================================================

elif st.session_state.stage == "love":

    st.markdown("""
    <style>
    .main-title {
        text-align:center;
        font-size:44px;
        color:#ff2d6f;
        font-weight:900;
        margin-bottom:20px;
        animation: glow 2s infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #ff99bb; }
        to { text-shadow: 0 0 25px #ff2d6f; }
    }
    .card {
        background: linear-gradient(180deg,#fff7fb,#fff1f6);
        padding:20px;
        border-radius:18px;
        margin-bottom:30px;
        box-shadow:0 10px 40px rgba(255,100,140,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>She Said YES 💖✨</div>", unsafe_allow_html=True)

    # 🎵 Background Music
    play_audio("songs/valentine.mp3")

    # 💌 Romantic Message
    st.markdown("""
    <div class='card'>
    From the first smile… to every little memory…  
    You have made my world softer, warmer, brighter.  

    Today isn’t just Valentine’s Day.  
    It’s the day I celebrate YOU.  

    And I promise —  
    I will always choose you. ❤️
    </div>
    """, unsafe_allow_html=True)

    # 📸 PHOTO GALLERY
    st.markdown("## Our Beautiful Moments 💞")

    cols = st.columns(2)

    images = [
        "images/v1.jpg",
        "images/v2.jpg",
        "images/v3.jpg",
        "images/v4.jpg"
    ]

    for i, img in enumerate(images):
        with cols[i % 2]:
            show_image(img)

    # 💖 Final Message
    st.markdown("""
    <div class='card'>
    You are my calm in chaos.  
    My happiness in ordinary days.  
    My favorite notification.  

    I love you more than words can explain. 💘
    </div>
    """, unsafe_allow_html=True)

    # 🎉 Confetti
    st.components.v1.html("""
    <canvas id="c" style="position:fixed;pointer-events:none;top:0;left:0;width:100%;height:100%;"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
    var myConfetti = confetti.create(document.getElementById('c'), { resize: true });
    myConfetti({ particleCount: 250, spread: 150 });
    </script>
    """, height=0)

    if st.button("🔄 Back to Proposal"):
        st.session_state.stage = "proposal"
        st.rerun()
