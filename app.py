# app.py
# Clean Valentine Loop Version (No Moving Button)

import streamlit as st
from PIL import Image, ImageOps
import requests, io, os, base64

# ---------------- CONFIG ----------------
REPO_OWNER = "its0su0rj"
REPO_NAME  = "owspracticeits-suraj"
BRANCH     = "main"

RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/"

st.set_page_config(page_title="For You ❤️", layout="wide")

# ---------------- FETCH HELPERS ----------------

def raw_url(path):
    return RAW_BASE + path

def try_fetch(path):
    try:
        r = requests.get(raw_url(path), timeout=10)
        if r.status_code == 200:
            return r.content
    except:
        return None
    return None

def fetch_image_auto(base):
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        b = try_fetch(f"images/{base}{ext}")
        if b:
            return b
    return None

def fetch_song_auto(base):
    for ext in [".mp3", ".wav", ".ogg"]:
        b = try_fetch(f"songs/{base}{ext}")
        if b:
            return b
    return None

def show_image(base):
    img_bytes = fetch_image_auto(base)
    if img_bytes:
        img = Image.open(io.BytesIO(img_bytes))
        img = ImageOps.exif_transpose(img)
        st.image(img, use_column_width=True)

def play_song(base):
    song = fetch_song_auto(base)
    if song:
        st.audio(song, format="audio/mp3")

# ---------------- SESSION ----------------

if "stage" not in st.session_state:
    st.session_state.stage = "proposal"

if "no_count" not in st.session_state:
    st.session_state.no_count = 0

# ======================================================
# 💘 STAGE 1 — PROPOSAL LOOP
# ======================================================

if st.session_state.stage == "proposal":

    st.markdown("""
    <style>
    .main-title {
        text-align:center;
        font-size:34px;
        font-weight:800;
        color:#ff2d6f;
        margin-bottom:30px;
    }
    .plead {
        text-align:center;
        font-size:20px;
        color:#c81d62;
        margin-bottom:20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>Nirali… will you be my Valentine? 💖</div>", unsafe_allow_html=True)

    # Pleading messages based on NO count
    if st.session_state.no_count == 1:
        st.markdown("<div class='plead'>Please bubuu say yes na 🥺💞</div>", unsafe_allow_html=True)

    elif st.session_state.no_count == 2:
        st.markdown("<div class='plead'>Please na babu say yes 🥺💖</div>", unsafe_allow_html=True)

    elif st.session_state.no_count >= 3:
        st.markdown("<div class='plead'>Areee kitna bhav khaogi 😭 Just say YES already 💘</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("YES 💘", use_container_width=True):
            st.session_state.stage = "love"
            st.rerun()

    with col2:
        if st.button("NO 😢", use_container_width=True):
            st.session_state.no_count += 1
            st.rerun()

# ======================================================
# 💕 STAGE 2 — LOVE PAGE (Auto Fetch Same Structure)
# ======================================================

elif st.session_state.stage == "love":

    # Background Music (songs/background.mp3)
    bg = fetch_song_auto("background")
    if bg:
        b64 = base64.b64encode(bg).decode()
        st.markdown(f"""
        <audio autoplay loop>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .main-title {
        text-align:center;
        font-size:44px;
        font-weight:900;
        color:#ff2d6f;
        margin-bottom:20px;
        animation: glow 2s infinite alternate;
    }
    @keyframes glow {
        from { text-shadow:0 0 10px #ff99bb; }
        to { text-shadow:0 0 30px #ff2d6f; }
    }
    .card {
        background:linear-gradient(180deg,#fff7fb,#fff1f6);
        padding:22px;
        border-radius:18px;
        margin-bottom:25px;
        box-shadow:0 10px 40px rgba(255,120,150,0.15);
        font-size:18px;
        color:#c81d62;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>finally yes😍, myyy bubuuuhhhh😘 💖✨</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
    From every memory we’ve shared…  
    to every smile you’ve given me…  

    You are my favorite part of life.  
    My calm. My happiness. My forever. 💘
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Our Beautiful Moments 💞")

    cols = st.columns(2)

    for i in range(1, 7):
        with cols[i % 2]:
            show_image(f"Page2.{i}")

    play_song("love")

    st.markdown("""
    <div class='card'>
    I don’t promise a perfect world…  
    but I promise to stand beside you in every imperfect one.  

    Happy Valentine’s Day ❤️  
    And thank you for choosing me.
    </div>
    """, unsafe_allow_html=True)

    st.components.v1.html("""
    <canvas id="c" style="position:fixed;pointer-events:none;top:0;left:0;width:100%;height:100%;"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
    var myConfetti = confetti.create(document.getElementById('c'), { resize: true });
    myConfetti({ particleCount: 300, spread: 160 });
    </script>
    """, height=0)

    if st.button("🔄 Restart"):
        st.session_state.stage = "proposal"
        st.session_state.no_count = 0
        st.rerun()
