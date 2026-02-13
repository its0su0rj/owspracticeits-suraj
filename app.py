# app.py
# Valentine Special – Auto Fetch Version (Compatible with your Birthday Repo)

import streamlit as st
from PIL import Image, ImageOps
import requests, io, os, base64, json

# ---------------- CONFIG (Same as your birthday app) ----------------
REPO_OWNER = "its0su0rj"
REPO_NAME  = "owspracticeits-suraj"
BRANCH     = "main"

RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/"

st.set_page_config(page_title="For You ❤️", layout="wide")

# ---------------- HELPERS (Same Logic as Before) ----------------

def raw_url(path):
    return RAW_BASE + path

def try_fetch_bytes(path):
    try:
        r = requests.get(raw_url(path), timeout=10)
        if r.status_code == 200:
            return r.content
    except:
        return None
    return None

def fetch_image_auto(base_name):
    exts = [".jpg", ".jpeg", ".png", ".webp"]
    for e in exts:
        b = try_fetch_bytes(f"images/{base_name}{e}")
        if b:
            return b
    return None

def fetch_song_auto(base_name):
    exts = [".mp3", ".wav", ".ogg"]
    for e in exts:
        b = try_fetch_bytes(f"songs/{base_name}{e}")
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

# =========================================================
# 💘 STAGE 1 — PERFECT PROPOSAL PAGE
# =========================================================
# =========================================================
# 💘 STAGE 1 — SMART PROPOSAL PAGE (Mobile Friendly)
# =========================================================

if st.session_state.stage == "proposal":

    proposal_html = """
    <style>
    .main-box {
        text-align:center;
        padding-top:80px;
        position:relative;
    }
    .title {
        font-size:30px;
        font-weight:800;
        color:#ff2d6f;
        margin-bottom:40px;
    }
    .btn {
        padding:14px 30px;
        font-size:18px;
        border:none;
        border-radius:14px;
        cursor:pointer;
        margin:15px;
        transition:0.2s ease;
    }
    .yes {
        background:#ff4d6d;
        color:white;
        box-shadow:0 8px 25px rgba(255,50,90,0.3);
    }
    .no {
        background:#444;
        color:white;
        position:absolute;
    }
    </style>

    <div class="main-box">
        <div class="title">
            Nirali… will you be my Valentine? 💖
        </div>

        <button class="btn yes" onclick="sendYes()">Yes 💘</button>
        <button class="btn no" id="noBtn">No 😢</button>
    </div>

    <script>
    let attempts = 0;
    const noBtn = document.getElementById("noBtn");

    // For Desktop (hover)
    noBtn.addEventListener("mouseover", moveButton);

    // For Mobile (touch)
    noBtn.addEventListener("touchstart", moveButton);

    function moveButton(e){
        if(attempts < 3){
            e.preventDefault();
            attempts++;
            const x = Math.random()*250 - 125;
            const y = Math.random()*150 - 75;
            noBtn.style.transform = `translate(${x}px, ${y}px)`;
        }
    }

    // After 3 attempts allow click
    noBtn.addEventListener("click", function(){
        if(attempts >= 3){
            document.querySelector(".main-box").innerHTML = `
                <div class="title">
                    Are you sure? 🥺💔
                </div>
                <button class="btn yes" onclick="sendYes()">
                    Okay fine… YES 💖
                </button>
            `;
        }
    });

    function sendYes(){
        window.parent.postMessage({type:'VALENTINE_YES'}, '*');
    }
    </script>
    """

    # Listen to JS message
    val = st.components.v1.html(proposal_html, height=500)

    # This hidden listener auto-refresh trick
    if "go_next" not in st.session_state:
        st.session_state.go_next = False

    # Invisible trigger using query param trick
    query_params = st.experimental_get_query_params()
    if "yes" in query_params:
        st.session_state.stage = "love"
        st.experimental_set_query_params()
        st.rerun()

    # JavaScript redirect helper
    st.components.v1.html("""
    <script>
    window.addEventListener("message", function(event){
        if(event.data.type === "VALENTINE_YES"){
            const url = new URL(window.location.href);
            url.searchParams.set("yes", "1");
            window.location.href = url.toString();
        }
    });
    </script>
    """, height=0)


    

# =========================================================
# 💕 STAGE 2 — BEAUTIFUL LOVE EXPERIENCE
# =========================================================

elif st.session_state.stage == "love":

    # Background Music (Auto fetch: songs/background.mp3)
    bg = fetch_song_auto("background")
    if bg:
        b64 = base64.b64encode(bg).decode()
        st.markdown(f"""
        <audio autoplay loop>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)

    # Elegant Styling
    st.markdown("""
    <style>
    .main-title {
        text-align:center;
        font-size:48px;
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

    st.markdown("<div class='main-title'>She Said YES 💖✨</div>", unsafe_allow_html=True)

    # Romantic Message
    st.markdown("""
    <div class='card'>
    From childhood memories… to today’s beautiful moments,  
    every phase of life feels warmer with you in it.  

    You are not just special.  
    You are my peace. My happiness. My forever. 💘
    </div>
    """, unsafe_allow_html=True)

    # Auto Image Gallery
    st.markdown("## Our Beautiful Moments 💞")

    cols = st.columns(2)

    for i in range(1, 7):  # will try Page2.1 ... Page2.6
        base_name = f"Page2.{i}"
        with cols[i % 2]:
            show_image(base_name)

    # Special Song Auto Fetch (songs/love.mp3)
    play_song("love")

    # Final Message
    st.markdown("""
    <div class='card'>
    I don’t promise perfect days…  
    but I promise to stay beside you on every imperfect one.  

    Happy Valentine’s Day ❤️  
    And thank you for choosing me.
    </div>
    """, unsafe_allow_html=True)

    # Confetti
    st.components.v1.html("""
    <canvas id="c" style="position:fixed;pointer-events:none;top:0;left:0;width:100%;height:100%;"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
    var myConfetti = confetti.create(document.getElementById('c'), { resize: true });
    myConfetti({ particleCount: 300, spread: 160 });
    </script>
    """, height=0)

    if st.button("⬅ Back"):
        st.session_state.stage = "proposal"
        st.rerun()
