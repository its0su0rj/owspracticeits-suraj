# app.py
# Final: loads images & songs directly from GitHub raw URLs for repo its0su0rj/owspracticeits-suraj
# Place this file in repo root. Ensure images/ and songs/ files exist in that repo.
import streamlit as st
from PIL import Image, ImageOps
import requests, io, os, json, base64

# --------------- CONFIG ---------------
REPO_OWNER = "its0su0rj"
REPO_NAME  = "owspracticeits-suraj"
BRANCH     = "main"   # change if your default branch is different

RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}/"

# UI / behavior
ITEMS_PER_PAGE = 4

st.set_page_config(page_title="🎉 Happy Birthday", layout="wide")

# --------------- CONTENT YOU WANTED ----------------
QUESTIONS_PAGE1 = [
    "1. In childhood you were cute or supercute? (Write 'cute' or 'supercute')",
    "2. Best duo... with whom? (Write 'ma' or 'life partner')",
    "3. Remember the first Rakhi trip — which colored top? (red or black)",
    "4. You looked gorgeous during Chhath — more beautiful in evening or morning?"
]
ANSWERS_PAGE1 = ["supercute", "ma", "red", "evening"]  # case-insensitive

# Prewritten romantic messages (auto-filled for pages 2..4)
MESSAGES_PAGE2 = [
    "Your intelligence sparkles like stars; your beauty only highlights it. You are flawless.",
    "Confidence and kindness — you wear them both effortlessly. I admire you every day.",
    "Your laugh breaks the clouds away — everything’s brighter with you in it.",
    "You are a radiant presence; the world is softer when you smile."
]
MESSAGES_PAGE3 = [
    "This memory is a warm lamp in my heart — forever glowing because of you.",
    "Every photo with you is a chapter of joy I read again and again.",
    "Your laughter in these moments still lives in my chest — soft and warm.",
    "I fall for you again in every memory; thank you for being my favorite."
]
MESSAGES_PAGE4 = [
    "The future looks golden because you will shine in everything you do.",
    "I see travel, laughter, growth and us — all painted with your light.",
    "You will achieve so much; your strength humbles and inspires me.",
    "We'll turn tiny moments into a grand love story — and I can't wait."
]

# Song hints / mapping for page1 (slot -> hint filename). We'll try multiple patterns for robustness.
SONG_HINTS_PAGE1 = ["song1.mp3", "song2.mp3", "song3.mp3", "song4.mp3"]
BACKGROUND_SONG = "background.mp3"
LAST_SONG = "lastsong.mp3"

# --------------- STYLING ---------------
st.markdown("""
<style>
.main-title {text-align:center; font-size:44px; color:#ff2d6f; font-weight:900; margin-bottom:6px;}
.subtitle {text-align:center; font-size:16px; color:#ff8fab; margin-bottom:14px;}
button[kind="primary"], button[kind="secondary"], .stButton>button {
  animation: heartbeat 1.6s infinite;
  border-radius: 12px !important;
  box-shadow: 0 8px 22px rgba(255,77,109,0.12);
  font-weight:700 !important;
}
.stButton>button:hover { box-shadow: 0 12px 34px rgba(255,50,90,0.2); transform: translateY(-3px); }
@keyframes heartbeat { 0% {transform: scale(1);} 25% {transform: scale(1.06);} 40% {transform: scale(0.98);} 60% {transform: scale(1.03);} 100% {transform: scale(1);} }
.glow-box { background: linear-gradient(180deg,#fff7fb,#fff1f6); padding:14px; border-radius:12px;
           box-shadow: 0 8px 30px rgba(255,120,150,0.06); border: 1px solid rgba(255,100,140,0.08);
           margin-bottom: 12px; }
.heart { position: fixed; bottom: 12px; left: 50%; transform: translateX(-50%); font-size:28px; z-index:9999; opacity:0.95;}
.sparkle { position: fixed; top:-10px; font-size:20px; color:#ffd6e8; z-index:9998; pointer-events:none; }
.typewriter { font-size:18px; color:#c81d62; font-weight:700; white-space: pre-wrap; }
.page-header { text-align:center; font-size:28px; color:#ff3b6b; margin-top:10px; margin-bottom:8px; font-weight:800; }
</style>
<div class="heart">💖</div>
<div class="sparkle" style="left:20%; animation: fall 6s linear infinite;">✨</div>
<div class="sparkle" style="left:40%; animation: fall 7s linear infinite;">🌟</div>
<div class="sparkle" style="left:60%; animation: fall 5.5s linear infinite;">💫</div>
""", unsafe_allow_html=True)

# --------------- HELPERS: fetch raw bytes from GitHub ---------------
def raw_url(path):
    """Return full raw URL for a file path in the repo."""
    return RAW_BASE + path

def try_fetch_bytes(path):
    """Try GET raw URL, return bytes if 200 else None."""
    url = raw_url(path)
    try:
        r = requests.get(url, timeout=12)
        if r.status_code == 200:
            return r.content
    except Exception:
        return None
    return None

def fetch_image_from_repo(base_name):
    """Try several variants for image: images/<base>.ext or images/<base_underscore>.ext"""
    exts = [".jpg", ".jpeg", ".png", ".webp"]
    candidates = []
    # prefer dot variant like Page1.1
    candidates += [f"images/{base_name}{e}" for e in exts]
    # underscore variant
    candidates += [f"images/{base_name.replace('.', '_')}{e}" for e in exts]
    for p in candidates:
        b = try_fetch_bytes(p)
        if b:
            return b, p  # bytes, path used
    return None, None

def fetch_song_from_repo(base_name):
    exts = [".mp3", ".wav", ".ogg"]
    # patterns to try: songs/<hint>, songs/<base>
    candidates = []
    candidates += [f"songs/{base_name}"]
    # if base_name has extension already, try as-is; otherwise add exts
    if os.path.splitext(base_name)[1]:
        candidates += [f"songs/{base_name}"]
    else:
        candidates += [f"songs/{base_name}{e}" for e in exts]
        candidates += [f"songs/{base_name.replace('.', '_')}{e}" for e in exts]
    for p in candidates:
        b = try_fetch_bytes(p)
        if b:
            return b, p
    return None, None

def stream_image_bytes(image_bytes):
    """Open bytes as PIL Image and show via st.image"""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img = ImageOps.exif_transpose(img)
        st.image(img, use_column_width=True)
    except Exception:
        st.error("Found image bytes but couldn't decode image.")

def stream_audio_bytes(audio_bytes):
    try:
        st.audio(audio_bytes, format="audio/mp3")
    except Exception:
        # fallback: try raw URL streaming (rare)
        st.error("Could not play audio bytes directly.")

# --------------- Background music injection (small floating player) ---------------
def inject_background_music():
    # try background in songs/background.mp3 or raw filename
    b, p = fetch_song_from_repo(BACKGROUND_SONG)
    if b:
        # embed base64 like earlier
        b64 = base64.b64encode(b).decode()
        html = f"""
        <audio autoplay loop controls style="position:fixed; bottom:16px; right:16px; width:260px; z-index:9999; opacity:0.92;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(html, unsafe_allow_html=True)

inject_background_music()

# --------------- Header and navigation ---------------
st.markdown("<div class='main-title'>🎉 Happy Birthday! 🎉</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A little interactive journey — unlock images, messages & songs ✨</div>", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    c1, c2, c3, c4, c5 = st.columns([1,1,1,1,0.6])
    with c1:
        if st.button("🌈 Journey", key="btn_journey"): st.session_state.page = "journey"
    with c2:
        if st.button("✨ Qualities", key="btn_qualities"): st.session_state.page = "qualities"
    with c3:
        if st.button("💞 Memories", key="btn_memories"): st.session_state.page = "memories"
    with c4:
        if st.button("🌟 Future", key="btn_future"): st.session_state.page = "future"
    with c5:
        if st.button("💌 My Last Message", key="btn_letter"): st.session_state.page = "letter"
if st.session_state.page == "home":
    st.info("Click any section to begin — Journey, Qualities, Memories, Future or My Last Message")

# --------------- Utility: safe typewriter HTML ---------------
def typewriter_html_safe(text, uid):
    js_text = json.dumps(text)  # safely escaped JS string
    html = f"""
    <div class="typewriter"><span id="{uid}"></span></div>
    <script>
      const txt = {js_text};
      const el = document.getElementById('{uid}');
      let i = 0;
      (function typeWriter(){{
        if(i < txt.length){{
          el.innerHTML += txt.charAt(i);
          i++;
          setTimeout(typeWriter, 18);
        }}
      }})();
    </script>
    """
    return html

# --------------- Reveal block for Page 1 (question -> reveal image+message+song) ---------------
def page1_block(slot_index):
    base_name = f"Page1.{slot_index}"  # this matches your filenames like Page1.1.jpg (case-sensitive)
    # We will try the exact casing user used (they uploaded files like Page1.1.jpg)
    question = QUESTIONS_PAGE1[slot_index - 1]
    correct = ANSWERS_PAGE1[slot_index - 1].lower()
    st.markdown("<div class='glow-box'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-weight:700; color:#c81d62; margin-bottom:6px;'>{question}</div>", unsafe_allow_html=True)
    key_in = f"p1_in_{slot_index}"
    key_btn = f"p1_btn_{slot_index}"
    key_rev = f"p1_rev_{slot_index}"
    user = st.text_input("", key=key_in, placeholder="Type the answer and press Submit")
    if st.button("Submit", key=key_btn):
        if user.strip().lower() == correct and correct != "":
            st.session_state[key_rev] = True
        else:
            st.error("Not quite — try again 🥺")
    if st.session_state.get(key_rev, False):
        # fetch image bytes from GitHub raw
        image_bytes, used_path = fetch_image_from_repo(base_name)
        if image_bytes:
            stream_image_bytes(image_bytes)
        else:
            st.info(f"Image not found in repo. Upload file at: images/{base_name}.jpg (or {base_name.replace('.', '_')}.jpg).")
        # message specific to page1 slot (crafted)
        page1_msgs = [
            "supercute❣️ This little you is the cutest 🌸🙂
             So innocent, so happy… it’s nice to see how beautifully you’ve grown while keeping the same sweet nature  ",
            "Your bond with Ma is woven of lullabies, warmth and unending care. That love made you who you are — tender, strong and luminous.",
            "That red top moment — the world paused: that color met your glow and created a sun that day. Pure fire.",
            "Evening lights wrap your face like poetry. No one captures dusk the way you do — soft, radiant and unforgettable."
        ]
        st.components.v1.html(typewriter_html_safe(page1_msgs[slot_index - 1], f"p1_msg_{slot_index}"), height=100)
        # song: try hint filename then base_name
        song_bytes, song_path = fetch_song_from_repo(SONG_HINTS_PAGE1[slot_index - 1])
        if not song_bytes:
            song_bytes, song_path = fetch_song_from_repo(f"song{slot_index}")  # song1, song2 etc
        if not song_bytes:
            song_bytes, song_path = fetch_song_from_repo(base_name)
        if song_bytes:
            stream_audio_bytes(song_bytes)
        else:
            st.info("No song found for this slot. Upload e.g. songs/song1.mp3 or songs/song1.1.mp3")
        # confetti
        st.components.v1.html("""
            <canvas id='c' style='position:fixed;pointer-events:none;top:0;left:0;width:100%;height:100%;'></canvas>
            <script src='https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js'></script>
            <script>
              var myConfetti = confetti.create(document.getElementById('c'), { resize: true, useWorker: true });
              myConfetti({particleCount: 200, spread: 150, origin: {y:0.6}});
            </script>
        """, height=0)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("")

# --------------- Pages 2..4 auto (no questions) ---------------
def page_auto(page_no, messages):
    title_map = {2: "✨ Qualities — The Magic You Carry", 3: "💞 Memories — Our Sweetest Moments", 4: "🌟 Future — A Beautiful Tomorrow Awaits"}
    st.markdown(f"<div class='page-header'>{title_map.get(page_no, 'Page')}</div>", unsafe_allow_html=True)
    for i in range(1, ITEMS_PER_PAGE + 1):
        base = f"Page{page_no}.{i}"
        st.markdown("<div class='glow-box'>", unsafe_allow_html=True)
        img_bytes, used_path = fetch_image_from_repo(base)
        if img_bytes:
            stream_image_bytes(img_bytes)
        else:
            st.info(f"Image missing: images/{base}.jpg (or underscore variant).")
        msg = messages[i-1] if i-1 < len(messages) else "You are wonderful in every way."
        st.components.v1.html(typewriter_html_safe(msg, f"auto_{page_no}_{i}"), height=90)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("")

# --------------- Last message page ---------------
def page_last():
    st.markdown("<div class='page-header'>💌 My Last Message For You</div>", unsafe_allow_html=True)
    # play lastsong if available
    b, p = fetch_song_from_repo(LAST_SONG)
    if not b:
        # try lastsong without extension or alternate names
        b, p = fetch_song_from_repo("lastsong")
    if b:
        stream_audio_bytes(b)
    else:
        st.info("Upload songs/lastsong.mp3 to play a special song here.")
    st.markdown("""
    <div style='background:linear-gradient(180deg,#fff7fb,#fff1f6); padding:22px; border-radius:12px;
                box-shadow:0 8px 30px rgba(255,120,150,0.08); font-size:18px; color:#b81c5a;'>
    ❤️ If love had a shape, it would be the warmth in your smile.<br><br>
    🌙 Every moment with you becomes a favorite memory stitched with laughter.<br><br>
    ✨ You are not only breathtaking — your mind, your courage, your kindness make you rare and endlessly precious.<br><br>
    🎀 I love you more than words; I wish you galaxies on your birthday and always. Happy Birthday. 💖
    </div>
    """, unsafe_allow_html=True)

# --------------- ROUTING ---------------
# Home: show big buttons
if st.session_state.get("page", "home") == "home":
    c1, c2, c3, c4, c5 = st.columns([1,1,1,1,0.6])
    with c1:
        if st.button("🌈 Journey", key="h_journey"): st.session_state.page = "journey"
    with c2:
        if st.button("✨ Qualities", key="h_qualities"): st.session_state.page = "qualities"
    with c3:
        if st.button("💞 Memories", key="h_memories"): st.session_state.page = "memories"
    with c4:
        if st.button("🌟 Future", key="h_future"): st.session_state.page = "future"
    with c5:
        if st.button("💌 My Last Message", key="h_letter"): st.session_state.page = "letter"

# Render chosen page
page = st.session_state.get("page", "home")
if page == "journey":
    st.markdown("<div class='page-header'>🌈 Journey — From Childhood to Today</div>", unsafe_allow_html=True)
    for s in range(1, ITEMS_PER_PAGE + 1):
        page1_block(s)
elif page == "qualities":
    page_auto(2, MESSAGES_PAGE2)
elif page == "memories":
    page_auto(3, MESSAGES_PAGE3)
elif page == "future":
    page_auto(4, MESSAGES_PAGE4)
elif page == "letter":
    page_last()

# back to home button
st.markdown("<hr/>", unsafe_allow_html=True)
if st.button("⬅️ Back to Home"):
    st.session_state.page = "home"
